# shortcuts.py
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
# SPDX-License-Identifier: MIT)

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gio, Gtk

def add_shortcuts(widget, settings):
    action_map = Gio.SimpleActionGroup.new()
    widget.insert_action_group("cavalier", action_map)
    shortcut_controller = Gtk.ShortcutController.new()
    shortcut_controller.set_scope(Gtk.ShortcutScope.MANAGED)
    widget.add_controller(shortcut_controller)

    act_next_mode = Gio.SimpleAction.new("next-mode", None)
    act_next_mode.connect('activate', change_mode, settings, 1)
    action_map.add_action(act_next_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("D"), \
        Gtk.NamedAction.new("cavalier.next-mode")))
    act_prev_mode = Gio.SimpleAction.new("prev-mode", None)
    act_prev_mode.connect('activate', change_mode, settings, -1)
    action_map.add_action(act_prev_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>D"), \
        Gtk.NamedAction.new("cavalier.prev-mode")))

    act_inc_margin = Gio.SimpleAction.new("increase-margin", None)
    act_inc_margin.connect('activate', change_setting, settings, 'margin', 1)
    action_map.add_action(act_inc_margin)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("N"), \
        Gtk.NamedAction.new("cavalier.increase-margin")))
    act_dec_margin = Gio.SimpleAction.new("decrease-margin", None)
    act_dec_margin.connect('activate', change_setting, settings, 'margin', -1)
    action_map.add_action(act_dec_margin)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>N"), \
        Gtk.NamedAction.new("cavalier.decrease-margin")))

    act_inc_offset = Gio.SimpleAction.new("increase-offset", None)
    act_inc_offset.connect('activate', change_setting, settings, \
        'items-offset', 1)
    action_map.add_action(act_inc_offset)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("O"), \
        Gtk.NamedAction.new("cavalier.increase-offset")))
    act_dec_offset = Gio.SimpleAction.new("decrease-offset", None)
    act_dec_offset.connect('activate', change_setting, settings, \
        'items-offset', -1)
    action_map.add_action(act_dec_offset)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>O"), \
        Gtk.NamedAction.new("cavalier.decrease-offset")))

    act_inc_roundness = Gio.SimpleAction.new("increase-roundness", None)
    act_inc_roundness.connect('activate', change_setting, settings, \
        'items-roundness', 1)
    action_map.add_action(act_inc_roundness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("R"), \
        Gtk.NamedAction.new("cavalier.increase-roundness")))
    act_dec_roundness = Gio.SimpleAction.new("decrease-roundness", None)
    act_dec_roundness.connect('activate', change_setting, settings, \
        'items-roundness', -1)
    action_map.add_action(act_dec_roundness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>R"), \
        Gtk.NamedAction.new("cavalier.decrease-roundness")))

    act_toggle_corners = Gio.SimpleAction.new("toggle-corners", None)
    act_toggle_corners.connect('activate', toggle_setting, settings, \
        'sharp-corners')
    action_map.add_action(act_toggle_corners)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("S"), \
        Gtk.NamedAction.new("cavalier.toggle-corners")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>S"), \
        Gtk.NamedAction.new("cavalier.toggle-corners")))

    act_toggle_controls = Gio.SimpleAction.new("toggle-controls", None)
    act_toggle_controls.connect('activate', toggle_setting, settings, \
        'window-controls')
    action_map.add_action(act_toggle_controls)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("H"), \
        Gtk.NamedAction.new("cavalier.toggle-controls")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>H"), \
        Gtk.NamedAction.new("cavalier.toggle-controls")))

    act_toggle_autohide = Gio.SimpleAction.new("toggle-autohide", None)
    act_toggle_autohide.connect('activate', toggle_setting, settings, \
        'autohide-header')
    action_map.add_action(act_toggle_autohide)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("A"), \
        Gtk.NamedAction.new("cavalier.toggle-autohide")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>A"), \
        Gtk.NamedAction.new("cavalier.toggle-autohide")))

    act_inc_bars = Gio.SimpleAction.new("increase-bars", None)
    act_inc_bars.connect('activate', change_setting, settings, 'bars', 2)
    action_map.add_action(act_inc_bars)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("B"), \
        Gtk.NamedAction.new("cavalier.increase-bars")))
    act_dec_bars = Gio.SimpleAction.new("decrease-bars", None)
    act_dec_bars.connect('activate', change_setting, settings, 'bars', -2)
    action_map.add_action(act_dec_bars)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>B"), \
        Gtk.NamedAction.new("cavalier.decrease-bars")))

    act_toggle_channels = Gio.SimpleAction.new("toggle-channels", None)
    act_toggle_channels.connect('activate', change_channels, settings)
    action_map.add_action(act_toggle_channels)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("C"), \
        Gtk.NamedAction.new("cavalier.toggle-channels")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>C"), \
        Gtk.NamedAction.new("cavalier.toggle-channels")))

    act_toggle_reverse = Gio.SimpleAction.new("toggle-reverse", None)
    act_toggle_reverse.connect('activate', toggle_setting, settings, \
        'reverse-order')
    action_map.add_action(act_toggle_reverse)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("E"), \
        Gtk.NamedAction.new("cavalier.toggle-reverse")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>E"), \
        Gtk.NamedAction.new("cavalier.toggle-reverse")))

    act_toggle_style = Gio.SimpleAction.new("toggle-style", None)
    act_toggle_style.connect('activate', change_widgets_style, settings)
    action_map.add_action(act_toggle_style)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("W"), \
        Gtk.NamedAction.new("cavalier.toggle-style")))
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>W"), \
        Gtk.NamedAction.new("cavalier.toggle-style")))

    act_next_profile = Gio.SimpleAction.new("next-profile", None)
    act_next_profile.connect('activate', change_color_profile, settings, 1)
    action_map.add_action(act_next_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("P"), \
        Gtk.NamedAction.new("cavalier.next-profile")))
    act_prev_profile = Gio.SimpleAction.new("prev-profile", None)
    act_prev_profile.connect('activate', change_color_profile, settings, -1)
    action_map.add_action(act_prev_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>P"), \
        Gtk.NamedAction.new("cavalier.prev-profile")))

def change_mode(action, parameter, settings, diff):
    modes = ['wave', 'levels', 'particles', 'bars']
    new_index = modes.index(settings.get('mode')) + diff
    if new_index > len(modes) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(modes) - 1
    settings.set('mode', modes[new_index])

def change_channels(action, parameter, settings):
    if settings.get('channels') == 'mono':
        settings.set('channels', 'stereo')
    else:
        settings.set('channels', 'mono')

def change_widgets_style(action, parameter, settings):
    if settings.get('widgets-style') == 'light':
        settings.set('widgets-style', 'dark')
    else:
        settings.set('widgets-style', 'light')

def change_color_profile(action, parameter, settings, diff):
    profiles = settings.get('color-profiles')
    new_index = settings.get('active-color-profile') + diff
    if new_index > len(profiles) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(profiles) - 1
    settings.set('active-color-profile', new_index)

def change_setting(action, parameter, settings, key, diff):
    settings.set(key, settings.get(key) + diff)

def toggle_setting(action, parameter, settings, key):
    settings.set(key, not settings.get(key))
