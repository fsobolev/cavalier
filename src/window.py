# window.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GObject

from .draw import wave, levels
from .cava import Cava
from threading import Thread

class CavalierWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CavalierWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cava_sample = []

        self.build_ui()
        self.connect('close-request', self.on_close_request)

        self.cava = Cava(self)
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()

        GObject.timeout_add(1000.0 / 60.0, self.redraw)

    def build_ui(self):
        self.overlay = Gtk.Overlay.new()
        self.set_content(self.overlay)

        self.drawing_area = Gtk.DrawingArea.new()
        self.drawing_area.set_vexpand(True)
        self.drawing_area.set_hexpand(True)
        self.drawing_area.set_draw_func(self.draw_func, None, None)
        self.overlay.set_child(self.drawing_area)

        self.header = Adw.HeaderBar.new()
        self.header.add_css_class('flat')
        self.header.set_decoration_layout('')
        self.header.set_title_widget(Gtk.Label.new(''))
        self.overlay.add_overlay(self.header)

        self.btn = Gtk.Button.new_from_icon_name('help-about-symbolic')
        self.btn.set_valign(Gtk.Align.START)
        self.header.pack_start(self.btn)

    def draw_func(self, area, cr, width, height, data, n):
        if len(self.cava_sample) > 0:
            levels(self.cava_sample, cr, width, height)

    def redraw(self):
        self.drawing_area.queue_draw()
        return True

    def on_close_request(self, w):
        self.cava.stop()
