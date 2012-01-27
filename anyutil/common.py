# -*- coding: utf-8 -*-
#
#  common.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-22.
#  Copyright 2012 Lars Yencken. All rights reserved.
#

"""
Common methods for command-line operation.
"""

import curses
import re

MAX_IO_RETRIES = 2

_color_pattern = re.compile("\x1b\[[0-9]*(;[0-9]*)?m", re.UNICODE)

def init_win(win):
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    win.nodelay(1)

def robust_line_iter(istream):
    "Read lines, continuing if a blocking system call gets interrupted."
    tries_since_success = 0
    sub = _color_pattern.sub

    lines = unbuffered_lines(istream)
    while True:
        try:
            l = lines.next()
            tries_since_success = 0

            # trim and remove shell colors
            l_no_color = sub(u'', l.rstrip())

            yield l_no_color

        except StopIteration:
            break

        except IOError:
            # sometimes we can get interrupted on a blocking read
            # let's retry a few times
            tries_since_success += 1

            if tries_since_success >= MAX_IO_RETRIES:
                # something's really wrong
                break

def unbuffered_lines(istream):
    "Read from the stream using the less-buffered readline() method."
    l = istream.readline()
    while l:
        yield l
        l = istream.readline()

def get_zoom(largest, width):
    """
    Determine an appropriate zoom ratio so that the given value will fit
    within width.
    """
    scale = 0
    options = [1, 2, 3, 5]

    while True:
        for x in options:
            zoom = x * (10**scale)
            if largest / zoom <= width:
                return zoom
        scale += 1

