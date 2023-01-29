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
from inspect import signature

class CavalierSettings(Gio.Settings):
    __gtype_name__ = 'CavalierSettings'

    def __init__(self):
        super().__init__(self)

    def new(callback_fn=None):
        gsettings = Gio.Settings.new('io.github.fsobolev.Cavalier')
        gsettings.__class__ = CavalierSettings
        if callback_fn:
            gsettings.connect('changed', gsettings.on_settings_changed)
            gsettings.callback_fn = callback_fn
            gsettings.callback_fn_sig_len = len(signature(callback_fn).parameters)
        return gsettings

    def on_settings_changed(self, obj, key):
        if self.callback_fn_sig_len > 0:
            self.callback_fn(key)
        else:
            self.callback_fn()
    
