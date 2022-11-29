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

from gi.repository import Adw, Gtk, Gio
from cavalier.settings import CavalierSettings


class CavalierPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'CavalierPreferencesWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_modal(False)
        self.settings = CavalierSettings.new()

        self.create_cavalier_page()
        self.create_cava_page()
        self.create_colors_page()

    def create_cavalier_page(self):
        self.cavalier_page = Adw.PreferencesPage.new()
        self.cavalier_page.set_title('Cavalier')
        self.cavalier_page.set_icon_name('image-x-generic-symbolic')
        self.add(self.cavalier_page)

        self.cavalier_mode_group = Adw.PreferencesGroup.new()
        self.cavalier_mode_group.set_title(_('Drawing Mode'))
        self.cavalier_page.add(self.cavalier_mode_group)

        self.wave_row = Adw.ActionRow.new()
        self.wave_row.set_title(_('Wave'))
        self.wave_check_btn = Gtk.CheckButton.new()
        self.wave_row.add_prefix(self.wave_check_btn)
        self.wave_row.set_activatable_widget(self.wave_check_btn)
        self.wave_check_btn.connect('toggled', self.on_save, 'mode', 'wave')
        self.cavalier_mode_group.add(self.wave_row)

        self.levels_row = Adw.ActionRow.new()
        self.levels_row.set_title(_('Levels'))
        self.levels_check_btn = Gtk.CheckButton.new()
        self.levels_check_btn.set_group(self.wave_check_btn)
        self.levels_row.add_prefix(self.levels_check_btn)
        self.levels_row.set_activatable_widget(self.levels_check_btn)
        self.levels_check_btn.connect('toggled', self.on_save, 'mode', 'levels')
        self.cavalier_mode_group.add(self.levels_row)

        self.bars_row = Adw.ActionRow.new()
        self.bars_row.set_title(_('Bars'))
        self.bars_check_btn = Gtk.CheckButton.new()
        self.bars_check_btn.set_group(self.wave_check_btn)
        self.bars_row.add_prefix(self.bars_check_btn)
        self.bars_row.set_activatable_widget(self.bars_check_btn)
        self.bars_check_btn.connect('toggled', self.on_save, 'mode', 'bars')
        self.cavalier_mode_group.add(self.bars_row)

        (self.wave_row, self.levels_row, self.bars_row)[ \
            ('wave', 'levels', 'bars').index(self.settings.get('mode')) \
            ].activate()

        self.cavalier_group = Adw.PreferencesGroup.new()
        self.cavalier_page.add(self.cavalier_group)

        self.pref_margin = Adw.ActionRow.new()
        self.pref_margin.set_title('Drawing area margin')
        self.pref_margin.set_subtitle( \
            _('Size of gaps around drawing area (in pixels).'))
        self.pref_margin_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 40.0, 1.0)
        self.pref_margin_scale.set_size_request(180, -1)
        self.pref_margin_scale.set_draw_value(True)
        self.pref_margin_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_margin_scale.set_value(self.settings.get("margin"))
        self.pref_margin_scale.connect('value-changed', self.on_save, \
            'margin', self.pref_margin_scale.get_value)
        self.pref_margin.add_suffix(self.pref_margin_scale)
        self.cavalier_group.add(self.pref_margin)

        self.pref_offset = Adw.ActionRow.new()
        self.pref_offset.set_title('Offset between items')
        self.pref_offset.set_subtitle( \
            _('The size of spaces between elements in "levels" and "bars" modes (in percent).'))
        self.pref_offset_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 20.0, 1.0)
        self.pref_offset_scale.set_size_request(180, -1)
        self.pref_offset_scale.set_draw_value(True)
        self.pref_offset_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_offset_scale.set_value(self.settings.get("items-offset"))
        self.pref_offset_scale.connect('value-changed', self.on_save, \
            'items-offset', self.pref_offset_scale.get_value)
        self.pref_offset.add_suffix(self.pref_offset_scale)
        self.cavalier_group.add(self.pref_offset)

        self.pref_sharp_corners = Adw.ActionRow.new()
        self.pref_sharp_corners.set_title('Sharp corners')
        self.pref_sharp_corners.set_subtitle( \
            _('Whether the main window corners should be sharp.'))
        self.pref_sharp_corners_switch = Gtk.Switch.new()
        self.pref_sharp_corners_switch.set_valign(Gtk.Align.CENTER)
        self.pref_sharp_corners_switch.set_active( \
            self.settings.get('sharp-corners'))
        # `state-set` signal returns additional argument that we don't need,
        # that's why lambda is used. Also GtkSwitch's state is changed after
        # signal, so we have to pass the opposite of ot
        self.pref_sharp_corners_switch.connect('state-set', \
            lambda *args : self.on_save(self.pref_sharp_corners_switch, \
                'sharp-corners', not self.pref_sharp_corners_switch.get_state()))
        self.pref_sharp_corners.add_suffix(self.pref_sharp_corners_switch)
        self.pref_sharp_corners.set_activatable_widget( \
            self.pref_sharp_corners_switch)
        self.cavalier_group.add(self.pref_sharp_corners)

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

    def on_save(self, w, key, value):
        if callable(value):
            value = value()
        if type(value) is float and type(self.settings.get(key)) is int:
            value = round(value)
        self.settings.set(key, value)
