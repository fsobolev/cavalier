# drawing_area.py
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
from cavalier.draw_functions import wave, line, levels, particles, bars
from cavalier.settings import CavalierSettings

class CavalierDrawingArea(Gtk.DrawingArea):
    __gtype_name__ = 'CavalierDrawingArea'

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

    def new():
        cda = Gtk.DrawingArea.new()
        cda.__class__ = CavalierDrawingArea
        cda.set_vexpand(True)
        cda.set_hexpand(True)
        cda.set_draw_func(cda.draw_func, None, None)
        cda.cava = None
        cda.spinner = None
        cda.settings = CavalierSettings.new(cda.on_settings_changed)
        cda.connect('unrealize', cda.on_unrealize)
        return cda

    def run(self):
        self.on_settings_changed(None)
        if self.cava == None:
            self.cava = Cava()
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()
        if self.spinner != None:
            self.spinner.set_visible(False)
        GObject.timeout_add(1000.0 / 60.0, self.redraw)

    def on_settings_changed(self, key):
        self.draw_mode = self.settings['mode']
        self.set_margin_top(self.settings['margin'])
        self.set_margin_bottom(self.settings['margin'])
        self.set_margin_start(self.settings['margin'])
        self.set_margin_end(self.settings['margin'])
        self.offset = self.settings['items-offset']
        self.roundness = self.settings['items-roundness']
        self.thickness = self.settings['line-thickness']
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
                'smoothing', 'noise-reduction'):
            if not self.cava.restarting:
                self.cava.stop()
                self.cava.restarting = True
                if self.spinner != None:
                    self.spinner.set_visible(True)
                    self.cava.sample = []
                GObject.timeout_add_seconds(3, self.run)

    def draw_func(self, area, cr, width, height, data, n):
        if len(self.cava_sample) > 0:
            if self.draw_mode == 'wave':
                wave(self.cava_sample, cr, width, height, self.colors)
            elif self.draw_mode == 'line':
                line(self.cava_sample, cr, width, height, self.colors, \
                    self.thickness)
            elif self.draw_mode == 'levels':
                levels(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.roundness)
            elif self.draw_mode == 'particles':
                particles(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.roundness)
            elif self.draw_mode == 'bars':
                bars(self.cava_sample, cr, width, height, self.colors, \
                    self.offset)

    def redraw(self):
        self.queue_draw()
        self.cava_sample = self.cava.sample
        if self.reverse_order:
            if self.channels == 'mono':
                self.cava_sample = self.cava_sample[::-1]
            else:
                self.cava_sample = \
                    self.cava_sample[0:int(len(self.cava_sample)/2):][::-1] + \
                    self.cava_sample[int(len(self.cava_sample)/2)::][::-1]
        return True

    def on_unrealize(self, obj):
        self.cava.stop()
