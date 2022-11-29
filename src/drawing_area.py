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

from gi.repository import Gtk, GObject, GdkPixbuf
from threading import Thread
from cavalier.cava import Cava
from cavalier.draw_functions import wave, levels, bars
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
        cda.settings = CavalierSettings.new(cda.on_settings_changed)
        return cda

    def run(self):
        self.apply_settings(False)
        self.connect('unrealize', self.on_unrealize)
        self.cava = Cava()
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()
        GObject.timeout_add(1000.0 / 60.0, self.redraw)

    def apply_settings(self, reload_cava=False):
        self.draw_mode = self.settings.get('mode')
        self.set_margin_top(self.settings.get('margin'))
        self.set_margin_bottom(self.settings.get('margin'))
        self.set_margin_start(self.settings.get('margin'))
        self.set_margin_end(self.settings.get('margin'))
        self.offset = self.settings.get('items-offset')
        self.colors = self.settings.get('fg-colors')
        if reload_cava:
            self.cava.reload()

    def on_settings_changed(self, key):
        if key in ('bars', 'channels', 'monstercat', 'monstercat-waves', \
                'noise-reduction'):
            self.apply_settings(True)
        else:
            self.apply_settings(False)

    def draw_func(self, area, cr, width, height, data, n):
        if len(self.cava_sample) > 0:
            if self.draw_mode == 'wave':
                wave(self.cava_sample, cr, width, height, self.colors)
            elif self.draw_mode == 'levels':
                levels(self.cava_sample, cr, width, height, self.colors, self.offset)
            elif self.draw_mode == 'bars':
                bars(self.cava_sample, cr, width, height, self.colors, self.offset)
            else:
                print(f'Error: Unknown drawing mode "{self.draw_mode}"')

    def redraw(self):
        self.queue_draw()
        self.cava_sample = self.cava.sample
        return True

    def on_unrealize(self, w):
        self.cava.stop()
