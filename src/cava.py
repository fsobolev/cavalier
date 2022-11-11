# cava.py
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

import os
import subprocess
import struct
import tempfile
import signal

BARS = 16

config = """
[general]
bars = 16
framerate = 60
[output]
method = raw
raw_target = /dev/stdout
bit_format = 16bit
[smoothing]
monstercat = 1
waves = 0
"""

class Cava:
    def __init__(self, cavalier_window):
        self.bytetype = "H"
        self.bytesize = 2
        self.bytenorm = 65535
        self.cavalier = cavalier_window
        self.running = False

    def run(self):
        self.running = True
        with tempfile.NamedTemporaryFile() as config_file:
            config_file.write(config.encode())
            config_file.flush()
            self.process = subprocess.Popen(["cava", "-p", config_file.name], stdout=subprocess.PIPE)
            chunk = self.bytesize * BARS
            fmt = self.bytetype * BARS
            source = self.process.stdout
            while True:
                data = source.read(chunk)
                if len(data) < chunk or not self.running:
                    break
                sample = [i / self.bytenorm for i in struct.unpack(fmt, data)]
                self.cavalier.cava_sample = sample
                self.cavalier.drawing_area.queue_draw()

    def stop(self):
        if self.running:
            self.running = False
            self.process.kill()

    def reload(self):
        if self.running:
            self.process.send_signal(signal.SIGUSR1)

