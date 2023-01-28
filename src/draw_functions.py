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
import cairo
import math

def set_source(cr, height, colors):
    if len(colors) > 1:
        pat = cairo.LinearGradient(0.0, 0.0, 0.0, height)
        for i in range(len(colors)):
            (red, green, blue, alpha) = colors[i]
            pat.add_color_stop_rgba(1 / (len(colors) - 1) * i, \
                red / 255, green / 255, blue / 255, alpha)
        cr.set_source(pat)
    else:
        (red, green, blue, alpha) = colors[0]
        cr.set_source_rgba(red / 255, green / 255, blue / 255, alpha)

def draw_element(cr, x, y, width, height, radius):
    degrees = math.pi / 180.0
    cr.new_sub_path()
    cr.arc(x + width * radius / 100, y + height * radius / 100, \
        radius * min(width, height) / 100, -180 * degrees, -90 * degrees)
    cr.arc(x + width - width * radius / 100, y + height * radius / 100, \
        radius * min(width, height) / 100, -90 * degrees, 0)
    cr.arc(x + width - width * radius / 100, y + height - height * radius / 100, \
        radius * min(width, height) / 100, 0, 90 * degrees)
    cr.arc(x + width * radius / 100, y + height - height * radius / 100, \
        radius * min(width, height) / 100, 90 * degrees, -180 * degrees)
    cr.close_path()

def wave(sample, cr, width, height, colors):
    set_source(cr, height, colors)
    ls = len(sample)
    cr.move_to(0, (1.0 - sample[0]) * height)
    for i in range(ls - 1):
        height_diff = (sample[i] - sample[i+1])
        cr.rel_curve_to(width / (ls - 1) * 0.5, 0.0, \
           width / (ls - 1) * 0.5, height_diff * height, \
           width / (ls - 1), height_diff * height)
    cr.line_to(width, height)
    cr.line_to(0, height)
    cr.fill()

def line(sample, cr, width, height, colors, thickness):
    set_source(cr, height, colors)
    ls = len(sample)
    cr.move_to(0, (1.0 - sample[0]) * height)
    cr.set_line_width(thickness)
    for i in range(ls - 1):
        height_diff = (sample[i] - sample[i+1])
        cr.rel_curve_to(width / (ls - 1) * 0.5, 0.0, \
           width / (ls - 1) * 0.5, height_diff * height, \
           width / (ls - 1), height_diff * height)
    cr.stroke()

def levels(sample, cr, width, height, colors, offset, radius):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    for i in range(ls):
        q = int(round(sample[i], 1) * 10)
        for r in range(q):
            draw_element(cr, step * i + offset_px, \
                height - (height / 10 * (r + 1)) + offset_px, \
                step - offset_px * 2, height / 10 - offset_px * 2, radius)
    cr.fill()

def particles(sample, cr, width, height, colors, offset, radius):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    for i in range(ls):
        draw_element(cr, step * i + offset_px, \
            height * 0.9 - height * 0.9 * sample[i] + offset_px, step - offset_px * 2, \
            height / 10 - offset_px * 2, radius)
    cr.fill()

def bars(sample, cr, width, height, colors, offset):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    for i in range(ls):
        cr.rectangle(step * i + offset_px, height - height * sample[i], \
            step - offset_px * 2, height)
    cr.fill()
