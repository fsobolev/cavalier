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

from gi.repository import Adw, Gtk, Gio, GObject

from cavalier.settings import CavalierSettings
from cavalier.drawing_area import CavalierDrawingArea
from cavalier.shortcuts import add_shortcuts


class CavalierWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CavalierWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = CavalierSettings.new(self.on_settings_changed)
        self.cava_sample = []

        self.build_ui()
        add_shortcuts(self, self.settings)
        self.connect('close-request', self.on_close_request)
        self.connect('notify::is-active', self.on_active_state_changed)

    def build_ui(self):
        self.set_title('Cavalier')
        self.set_size_request(170, 170)
        (width, height) = self.settings['size']
        self.set_default_size(width, height)
        if self.settings['maximized']:
            self.maximize()

        self.set_name('cavalier-window')
        self.toggle_sharp_corners()
        self.set_style()
        self.css_provider = Gtk.CssProvider.new()
        self.apply_colors()

        self.overlay = Gtk.Overlay.new()
        self.set_content(self.overlay)

        self.main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.main_box.set_hexpand(True)
        self.main_box.set_vexpand(True)
        self.overlay.add_overlay(self.main_box)

        self.header = Adw.HeaderBar.new()
        self.header.add_css_class('flat')
        self.header.set_show_start_title_buttons( \
            self.settings['window-controls'])
        self.header.set_show_end_title_buttons(self.settings['window-controls'])
        self.header.set_title_widget(Gtk.Label.new(''))
        self.main_box.append(self.header)

        self.handle = Gtk.WindowHandle.new()
        self.handle.set_hexpand(True)
        self.handle.set_vexpand(True)
        self.main_box.append(self.handle)

        self.bin_spinner = Adw.Bin.new()
        self.bin_spinner.set_hexpand(True)
        self.bin_spinner.set_vexpand(True)
        self.handle.set_child(self.bin_spinner)

        self.spinner = Gtk.Spinner.new()
        self.spinner.set_spinning(True)
        self.spinner.set_size_request(50, -1)
        self.spinner.set_halign(Gtk.Align.CENTER)
        self.spinner.set_margin_bottom(46) # headerbar height
        self.bin_spinner.set_child(self.spinner)

        self.drawing_area = CavalierDrawingArea.new()
        self.drawing_area.spinner = self.spinner
        self.drawing_area.run()
        self.overlay.set_child(self.drawing_area)

        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_valign(Gtk.Align.START)
        self.menu_button.set_icon_name('open-menu-symbolic')
        self.header.pack_start(self.menu_button)

        self.menu = Gio.Menu.new()
        self.menu.append(_('Preferences'), 'app.preferences')
        self.menu.append(_('Keyboard Shortcuts'), 'app.shortcuts')
        self.menu.append(_('About'), 'app.about')
        self.menu.append(_('Quit'), 'app.quit')
        self.menu_button.set_menu_model(self.menu)

    def set_style(self):
        if self.settings['widgets-style'] == 'light':
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def toggle_sharp_corners(self):
        if self.settings['sharp-corners']:
            self.add_css_class('sharp-corners')
        else:
            self.remove_css_class('sharp-corners')

    def apply_colors(self):
        try:
            color_profile = self.settings['color-profiles'][ \
                self.settings['active-color-profile']]
            colors = color_profile[2]
        except:
            colors = []
        if len(colors) == 0:
            self.get_style_context().remove_provider(self.css_provider)
        elif len(colors) == 1:
            self.css_data = '''#cavalier-window {
                background-color: rgba(%d, %d, %d, %f);
            }''' % colors[0]
            self.css_provider.load_from_data(self.css_data, -1)
            self.get_style_context().add_provider(self.css_provider, \
                Gtk.STYLE_PROVIDER_PRIORITY_USER)
        elif len(colors) > 1:
            self.css_data = '''#cavalier-window {
                background: linear-gradient(to bottom, '''
            for c in colors:
                self.css_data += 'rgba(%d, %d, %d, %f), ' % c
            self.css_data = self.css_data[:-2]
            self.css_data += ');}'
            self.css_provider.load_from_data(self.css_data, -1)
            self.get_style_context().add_provider(self.css_provider, \
                Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_settings_changed(self):
        self.header.set_show_start_title_buttons( \
            self.settings['window-controls'])
        self.header.set_show_end_title_buttons(self.settings['window-controls'])
        self.toggle_sharp_corners()
        self.set_style()
        self.apply_colors()
        try:
            self.on_active_state_changed()
        except:
            pass

    def on_close_request(self, obj):
        (width, height) = self.get_default_size()
        self.settings['size'] = (width, height)
        self.settings['maximized'] = self.is_maximized()
        if hasattr(self.get_application(), 'pref_win'):
            self.get_application().pref_win.close()

    def hide_header(self):
        if not self.is_active():
            self.header.set_show_start_title_buttons(False)
            self.header.set_show_end_title_buttons(False)
            self.menu_button.set_visible(False)
        return False # we don't need to restart the function

    def on_active_state_changed(self, *args):
        if self.settings['autohide-header'] and not self.is_active():
            # The window becomes inactive for a moment when
            # the menu button is pressed, making it impossible
            # to open the menu, so the delay is required
            GObject.timeout_add(100, self.hide_header)
        else:
            self.header.set_show_start_title_buttons( \
                self.settings['window-controls'])
            self.header.set_show_end_title_buttons( \
                self.settings['window-controls'])
            self.menu_button.set_visible(True)

