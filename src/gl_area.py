# gl_area.py
#
# Copyright 2022 Fyodor Sobolev
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.
#
# SPDX-License-Identifier: MIT

from gi.repository import Gtk, GObject
from threading import Thread
from cavalier.cava import Cava
from cavalier.draw_functions import wave, levels, particles, spine, bars
from cavalier.settings import CavalierSettings

import moderngl
import cairo

class CavalierGLArea(Gtk.GLArea):
    __gtype_name__ = 'CavalierGLArea'

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

    def new():
        cgla = Gtk.GLArea.new()
        cgla.__class__ = CavalierGLArea
        cgla.set_vexpand(True)
        cgla.set_hexpand(True)
        cgla.cava = None
        cgla.spinner = None
        cgla.settings = CavalierSettings.new(cgla.on_settings_changed)
        cgla.connect('realize', cgla.on_realize)
        cgla.connect('render', cgla.on_render)
        cgla.connect('unrealize', cgla.on_unrealize)

        return cgla

    def run(self):
        print('Using GPU')
        self.on_settings_changed(None)
        if self.cava == None:
            self.cava = Cava()
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()
        if self.spinner != None:
            self.spinner.set_visible(False)
        GObject.timeout_add(1000.0 / 60.0, self.render)

    def on_settings_changed(self, key):
        self.draw_mode = self.settings['mode']
        self.set_margin_top(self.settings['margin'])
        self.set_margin_bottom(self.settings['margin'])
        self.set_margin_start(self.settings['margin'])
        self.set_margin_end(self.settings['margin'])
        self.offset = self.settings['items-offset']
        self.roundness = self.settings['items-roundness']
        self.thickness = self.settings['line-thickness']
        self.fill = self.settings['fill']
        self.reverse_order = self.settings['reverse-order']
        self.channels = self.settings['channels']
        try:
            color_profile = self.settings['color-profiles'][ \
                self.settings['active-color-profile']]
            self.colors = color_profile[1]
        except:
            self.colors = []
        if len(self.colors) == 0:
            self.settings['color-profiles'] = [(_('Default'), \
                [(53, 132, 228, 1.0)], [])]
            return

        if key in ('bars', 'autosens', 'sensitivity', 'channels', \
                'smoothing', 'noise-reduction', 'gpu-accel'):
            if not self.cava.restarting:
                self.cava.stop()
                self.cava.restarting = True
                if self.spinner != None:
                    self.spinner.set_visible(True)
                    self.cava.sample = []
                GObject.timeout_add_seconds(3, self.run)

    def on_realize(self, area):
        area.make_current()
        self.ctx = moderngl.create_context(standalone=True)

    def render(self):
        self.on_render(self, self.ctx)
        return True

    def on_render(self, area, context):
        self.queue_render()
        self.cava_sample = self.cava.sample
        if self.reverse_order:
            if self.channels == 'mono':
                self.cava_sample = self.cava_sample[::-1]
            else:
                self.cava_sample = \
                    self.cava_sample[0:int(len(self.cava_sample)/2):][::-1] + \
                    self.cava_sample[int(len(self.cava_sample)/2)::][::-1]

        self.texture = self.render_to_texture(area.get_width(), area.get_height())
        self.texture.use()
        #self.screen_rectangle.render(mode=moderngl.TRIANGLE_STRIP)

    def on_unrealize(self, area):
        self.cava.stop()
        self.texture.release()

    def render_to_texture(self, width, height):

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        if len(self.cava_sample) > 0:
            if self.draw_mode == 'wave':
                wave(self.cava_sample, ctx, width, height, self.colors, \
                    self.fill, self.thickness)
            elif self.draw_mode == 'levels':
                levels(self.cava_sample, ctx, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'particles':
                particles(self.cava_sample, ctx, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'spine':
                spine(self.cava_sample, ctx, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'bars':
                bars(self.cava_sample, ctx, width, height, self.colors, \
                    self.offset, self.fill, self.thickness)

        texture = self.ctx.texture((width, height), 4, data=surface.get_data())
        texture.swizzle = 'BGRA' # use Cairo channel order (alternatively, the shader could do the swizzle)
        return texture
