# settings.py
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

from gi.repository import Gio, GLib

gsettings = Gio.Settings.new('io.github.fsobolev.Cavalier')
callback_fn = None

def get(key):
    return gsettings.get_value(key).unpack()

def set(key, value):
    if type(value) == int:
        gsettings.set_int32(key, value)
    elif type(value) == float:
        gsettings.set_double(key, value)
    elif type(value) == str:
        gsettings.set_string(key, value)
    elif type(value) == bool:
        gsettings.set_boolean(key, value)
    elif type(value) == tuple:
        gsettings.set_value(key, GLib.Variant.new_tuple(*value))
    else:
        print("Error: Can't identify type of the value " + value)

def on_settings_changed(s, key):
    if key in ('bars', 'channels', 'monstercat', 'monstercat-waves', \
            'noise-reduction'):
        callback_fn(True)
    else:
        callback_fn(False)

gsettings.connect('changed', on_settings_changed)
