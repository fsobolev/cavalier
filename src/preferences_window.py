# preferences_window.py
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

from gi.repository import Adw, Gtk

import cavalier.settings as settings


class CavalierPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'CavalierPreferencesWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_modal(False)

        self.create_cavalier_page()
        self.create_cava_page()
        self.create_colors_page()

    def create_cavalier_page(self):
        self.cavalier_page = Adw.PreferencesPage.new()
        self.cavalier_page.set_title('Cavalier')
        self.cavalier_page.set_icon_name('image-x-generic-symbolic')
        self.add(self.cavalier_page)

        self.cavalier_group = Adw.PreferencesGroup.new()
        self.cavalier_page.add(self.cavalier_group)

        self.pref_mode = Adw.ActionRow.new()
        self.pref_mode.set_title(_('Drawing mode'))
        self.pref_mode.set_subtitle( \
            _('Defines what the visualizer looks like.'))
        self.cavalier_group.add(self.pref_mode)

        self.pref_margin = Adw.ActionRow.new()
        self.pref_margin.set_title('Drawing area margin')
        self.pref_margin.set_subtitle( \
            _('Size of gaps around drawing area (in pixels)'))
        self.cavalier_group.add(self.pref_margin)

        self.pref_offset = Adw.ActionRow.new()
        self.pref_offset.set_title('Offset between items')
        self.pref_offset.set_subtitle( \
            _('The size of spaces between elements in "levels" and "bars" modes (in percent).'))
        self.cavalier_group.add(self.pref_offset)


    def create_cava_page(self):
        self.cava_page = Adw.PreferencesPage.new()
        self.cava_page.set_title('CAVA')
        self.cava_page.set_icon_name('utilities-terminal-symbolic')
        self.add(self.cava_page)

    def create_colors_page(self):
        self.colors_page = Adw.PreferencesPage.new()
        self.colors_page.set_title(_('Colors'))
        self.colors_page.set_icon_name('applications-graphics-symbolic')
        self.add(self.colors_page)
