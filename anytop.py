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
Live updating frequency distributions on streaming data.
"""

import os
import sys
import optparse
import curses
import time
import threading
import heapq
import re
import logging
from collections import defaultdict

if os.path.exists('debug.log'):
    os.remove('debug.log')

def anytop(win, debug=False):
    if debug:
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    dist = defaultdict(int)
    lock = threading.Lock()
    quit = threading.Event()
    logging.debug('Starting UI thread')
    ui = AnyTopUI(win, dist, lock)
    ui.start()
    m = re.compile("\x1b\[[0-9]*(;[0-9]*)?m", re.UNICODE)

    win.nodelay(1)

    try:
        for line in sys.stdin:
            key = m.sub('', line.rstrip())
            logging.debug('INPUT: requesting lock')
            lock.acquire()
            logging.debug('INPUT: lock acquired')
            try:
                if quit.is_set():
                    lock.release()
                    logging.debug('INPUT: lock released')
                    return
                dist[key] += 1
            finally:
                lock.release()
                logging.debug('INPUT: lock released')

        logging.debug('INPUT: finished')

        while True:
            time.sleep(3600)

    except KeyboardInterrupt:
        logging.debug('INPUT: got CTRL-C')
        ui.stop()
        ui.join()

    finally:
        ui.stop()
        ui.join()


class AnyTopUI(threading.Thread):
    'The ncurses user interface thread.'
    def __init__(self, win, dist, lock):
        self.win = win
        self.dist = dist
        self.lock = lock
        self._stop = threading.Event()
        super(AnyTopUI, self).__init__()
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()
    
    def run(self):
        while True:
            if self.stopped():
                return
            logging.debug('UI: requesting lock')
            self.lock.acquire()
            logging.debug('UI: lock acquired')
            self.refresh_display()
            self.lock.release()
            logging.debug('UI: lock released')
            time.sleep(1)

    def refresh_display(self):
        "Redraw the screen with the current data."
        logging.debug('UI: refreshing the display')
        height, width = self.win.getmaxyx()
        logging.debug('UI: size is %d x %d' % (width, height))
        d = self.dist
        n = len(d)
        s = sum(d.itervalues())
        
        largest_keys = heapq.nlargest(min(n, height - 2), d, key=d.__getitem__)
        largest = [(d[l], l) for l in largest_keys]

        logging.debug('UI: redraw call')
        self.win.redrawwin()
        self.win.addstr(0, 0, '%d keys, %d counts' % (n, s))
        if largest:
            w = max(6, len(str(max(c for (c, k) in largest))))
            k_len = width - w - 4
            template = ' %%%dd  %%s' % w
            for i, (c, k) in enumerate(largest):
                line = template % (c, k[:k_len])
                line += ' ' * (width - len(line) - 1)
                self.win.addstr(i + 2, 0, line)

        logging.debug('UI: refresh')
        self.win.refresh()

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options]

Live updating frequency distributions on streaming data. Like top, but for any
line-by-line input."""

    parser = optparse.OptionParser(usage)
    parser.add_option('--debug', action='store_true', dest='debug',
            help='Enable debug logging.')

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    curses.wrapper(anytop, debug=options.debug)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

