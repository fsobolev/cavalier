# draw.py
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
from gi.repository import Gdk, GdkPixbuf

def set_source(cr):
    cr.set_source_rgba(0, 0, 0, 0.5)
    # pb = GdkPixbuf.Pixbuf.new_from_file(os.getenv('XDG_CONFIG_HOME') + '/cavalier/pattern.png')
    # pb = pb.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
    # Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)

def wave(sample, cr, width, height):
    set_source(cr)
    ls = len(sample)
    cr.move_to(0, (1.0 - sample[0]) * height)
    for i in range(ls - 1):
        height_diff = (sample[i] - sample[i+1])
        cr.rel_curve_to(width / (ls - 1) * 0.5, 0.0, \
           width / (ls - 1) * 0.5, height_diff * height, \
           width / (ls - 1), height_diff * height)
    cr.line_to(width, height)
    cr.line_to(0, height)
    cr.close_path()
    cr.fill()

def levels(sample, cr, width, height, offset=10):
    set_source(cr)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    for i in range(ls):
        q = int(round(sample[i], 1) * 10)
        for r in range(q):
            cr.rectangle(step * i + offset_px, \
                height - (height / 10 * (r + 1)) + offset_px, \
                step - offset_px * 2, height / 10 - offset_px * 2)
    cr.fill()
