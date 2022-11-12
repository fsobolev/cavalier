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
import signal


class Cava:
    def __init__(self, cavalier_window):
        self.bytetype = "H"
        self.bytesize = 2
        self.bytenorm = 65535
        self.cavalier = cavalier_window
        self.running = False

        # Cava config options
        self.bars = 16
        self.channels = 'stereo'
        self.monstercat = 1
        self.waves = 0
        self.noise_reduction = 0.77

        if os.getenv('XDG_CONFIG_HOME'):
            self.config_dir = os.getenv('XDG_CONFIG_HOME') + '/cavalier'
        else:
            self.config_dir = os.getenv('HOME') + '/.config/cavalier'
        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file_path = self.config_dir + '/config'
        self.write_config()

    def run(self):
        self.running = True
        self.process = subprocess.Popen(["cava", "-p", self.config_file_path], \
            stdout=subprocess.PIPE)
        source = self.process.stdout
        self.reading_preparation()
        while True:
            data = source.read(self.chunk)
            if len(data) < self.chunk or not self.running:
                break
            sample = [i / self.bytenorm for i in struct.unpack(self.fmt, data)]
            self.cavalier.cava_sample = sample

    def reading_preparation(self):
        self.chunk = self.bytesize * self.bars
        self.fmt = self.bytetype * self.bars

    def stop(self):
        if self.running:
            self.running = False
            self.process.kill()

    def reload(self):
        if self.running:
            self.reading_preparation()
            self.process.send_signal(signal.SIGUSR1)

    def write_config(self):
        try:
            f = open(self.config_file_path, 'w')
            conf = '\n'.join([
                '[general]',
                f'bars = {self.bars}',
                'framerate = 60',
                '[input]',
                'method = pulse',
                '[output]',
                f'channels = {self.channels}',
                'mono_option = average',
                'method = raw',
                'raw_target = /dev/stdout',
                'bit_format = 16bit',
                '[smoothing]',
                f'monstercat = {self.monstercat}',
                f'waves = {self.waves}',
                f'noise_reduction = {self.noise_reduction}'
            ])
            f.write(conf)
            f.close()
        except Exception as e:
            print("Can't write config file for cava...'")
            print(e)

