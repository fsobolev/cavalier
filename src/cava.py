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
from cavalier.settings import CavalierSettings

class Cava:
    def __init__(self):
        self.BYTETYPE = "H"
        self.BYTESIZE = 2
        self.BYTENORM = 65535
        self.restarting = False

        self.settings = CavalierSettings.new()

        self.sample = []

        if os.getenv('XDG_CONFIG_HOME'):
            self.config_dir = os.getenv('XDG_CONFIG_HOME') + '/cavalier'
        else:
            self.config_dir = os.getenv('HOME') + '/.config/cavalier'
        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file_path = self.config_dir + '/config'

    def run(self):
        self.load_settings()
        self.write_config()
        self.process = subprocess.Popen(["cava", "-p", self.config_file_path], \
            stdout=subprocess.PIPE)
        source = self.process.stdout
        self.restarting = False
        self.chunk = self.BYTESIZE * self.bars
        self.fmt = self.BYTETYPE * self.bars
        while True:
            data = source.read(self.chunk)
            if len(data) < self.chunk or self.restarting:
                break
            self.sample = \
                [i / self.BYTENORM for i in struct.unpack(self.fmt, data)]

    def stop(self):
        if not self.restarting:
            self.process.kill()

    def load_settings(self):
        # Cava config options
        self.bars = self.settings['bars']
        self.autosens = int(self.settings['autosens'])
        self.sensitivity = self.settings['sensitivity']
        self.channels = self.settings['channels']
        self.monstercat = \
            ['off', 'monstercat'].index(self.settings['smoothing'])
        self.noise_reduction = self.settings['noise-reduction']

    def write_config(self):
        try:
            f = open(self.config_file_path, 'w')
            conf = '\n'.join([
                '[general]',
                f'bars = {self.bars}',
                f'autosens = {self.autosens}',
                f'sensitivity = {self.sensitivity ** 2}',
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
                f'noise_reduction = {self.noise_reduction}'
            ])
            f.write(conf)
            f.close()
        except Exception as e:
            print("Can't write config file for cava...'")
            print(e)

