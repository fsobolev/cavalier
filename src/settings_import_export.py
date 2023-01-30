# settings_import_export.py
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

import subprocess
from gi.repository import Adw

def import_settings(window, path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line != '\n':
                    subprocess.run(['gsettings', 'set', \
                        'io.github.fsobolev.Cavalier', line.split(' ')[0], \
                        line.replace(line.split(' ')[0], '').strip()])
        toast_msg = 'Settings sucessfully imported'

    except Exception as e:
        print('Can\'t import settings from file: ' + path)
        print(e)
        toast_msg = 'Failed to import settings'

    Adw.PreferencesWindow.add_toast(window, Adw.Toast.new(toast_msg))


def export_settings(window, path):
    gsettings_list = subprocess.run( \
        ['gsettings', 'list-recursively', 'io.github.fsobolev.Cavalier'], \
        stdout=subprocess.PIPE).stdout.decode('utf-8')
    try:
        with open(path, 'w') as file:
            for line in gsettings_list.split('\n'):
                file.write(' '.join(line.split(' ')[1::]) + '\n')
        toast_msg = 'File successfully saved'

    except Exception as e:
        print('Can\'t export settings to file: ' + path)
        print(e)
        toast_msg = 'Failed to save file'

    Adw.PreferencesWindow.add_toast(window, Adw.Toast.new(toast_msg))
