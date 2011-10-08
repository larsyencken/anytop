#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  anytop.py
#  anytop
#
#  Created by Lars Yencken on 2011-09-22.
#  Copyright 2011 Lars Yencken. All rights reserved.
#

"""
"""

import sys
import optparse
import curses
import time
import threading
import heapq
import re

from collections import Counter

def anytop(win):
    c = Counter()
    l = threading.Lock()
    alive = True
    ui = AnyTopUI(win, c, alive, l)
    ui.start()
    m = re.compile("\x1b\[[0-9]*(;[0-9]*)?m", re.UNICODE)

    try:
        for line in sys.stdin:
            line = m.sub('', line.rstrip())
            l.acquire()
            if not alive:
                l.release()
                return
            c[line.rstrip()] += 1
            l.release()

        ui.join()
    except KeyboardInterrupt:
        l.acquire()
        alive = False
        l.release()

class AnyTopUI(threading.Thread):
    def __init__(self, win, dist, alive, lock):
        self.win = win
        self.dist = dist
        self.alive = alive
        self.lock = lock

        super(AnyTopUI, self).__init__()
    
    def run(self):
        while True:
            self.lock.acquire()
            if not self.alive:
                self.lock.release()
                return

            self.refresh_display()
            self.lock.release()
            time.sleep(1)

    def refresh_display(self):
        height, width = self.win.getmaxyx()
        d = self.dist
        n = len(d)
        s = sum(d.itervalues())
        
        largest_keys = heapq.nlargest(min(n, height - 2), d, key=d.__getitem__)
        largest = [(d[l], l) for l in largest_keys]

        self.win.addstr(0, 0, '%d keys, %d counts' % (n, s))
        if largest:
            w = len(str(max(c for (c, k) in largest)))
            k_len = width - w - 1
            template = '%%%dd %%s' % w
            for i, (c, k) in enumerate(largest):
                line = template % (c, k[:k_len])
                line += ' ' * (width - len(line) - 1)
                self.win.addstr(i + 2, 0, line)

        self.win.refresh()

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options]

Insert usage message."""

    parser = optparse.OptionParser(usage)

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    curses.wrapper(anytop, *args)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

