#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  top.py
#  anytop
#

"""
Live updating frequency distributions on streaming data.
"""

import os
import sys
import curses
import time
import threading
import heapq
import logging
import codecs
import locale

import click

from anytop import (
    common,
    accumulate
)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def anytop(win, istream=sys.stdin, n=None):
    "Visualize the incoming lines by their distribution."
    if sys.version_info.major == 2:
        istream = codecs.getreader('utf8')(istream)
    common.init_win(win)
    if n:
        accumulator = accumulate.WindowAccumulator(n)
    else:
        accumulator = accumulate.Accumulator()
    lock = threading.Lock()
    logging.debug('Starting UI thread')
    ui = AnyTopUI(win, lock, accumulator)
    ui.start()

    try:
        for line in common.robust_line_iter(istream):
            if ui.error:
                return ui.error

            logging.debug('INPUT: requesting lock')
            lock.acquire()
            logging.debug('INPUT: lock acquired')
            accumulator.consume(line)
            lock.release()
            logging.debug('INPUT: lock released')

        logging.debug('INPUT: finished')

        # wait for CTRL-C
        # XXX we should display that the input was exhausted
        logging.debug('INPUT: exhausted')
        while True:
            time.sleep(3600)

    except KeyboardInterrupt:
        logging.debug('INPUT: got CTRL-C')
        ui.stop()
        ui.join()

    finally:
        ui.stop()
        ui.join()

    return ui.error


class AnyTopUI(threading.Thread):
    'The ncurses user interface thread.'
    def __init__(self, win, lock, accumulator):
        self.win = win
        self.acc = accumulator
        self.lock = lock
        self.error = None
        self._stop_event = threading.Event()
        super(AnyTopUI, self).__init__()

    def stop(self):
        logging.debug('UI: flagged as stopped')
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        try:
            while not self.stopped():
                logging.debug('UI: requesting lock')

                self.lock.acquire()
                logging.debug('UI: lock acquired')
                dist = self.acc.to_dist()
                logging.debug('UI: lock released')
                self.lock.release()

                self.refresh_display(dist)
                time.sleep(1)

        except Exception as e:
            self.lock.release()
            self.error = e
            return

    def refresh_display(self, d):
        "Redraw the screen with the current data."
        logging.debug('UI: refreshing the display')
        self.win.erase()
        height, width = self.win.getmaxyx()
        logging.debug('UI: size is %d x %d' % (width, height))

        n = len(d)
        s = sum(d.values())

        largest_keys = heapq.nlargest(min(n, height - 2), d, key=d.__getitem__)
        largest = [(d[l], l) for l in largest_keys]

        logging.debug('UI: redraw call')
        self.win.redrawwin()
        self.win.addstr(0, 0, '%d keys, %d counts' % (n, s))
        if largest:
            w = max(6, len(str(max(c for (c, k) in largest))))
            k_len = width - w - 4
            template = u' %%%dd  %%s' % w
            for i, (c, k) in enumerate(largest):
                line = (template % (c, k[:k_len]))[:width]
                try:
                    self.win.addstr(i + 2, 0, line.encode('utf8'))
                except:
                    raise Exception("couldn't draw: '%s'"
                                    % line.encode('utf8'))

        logging.debug('UI: refresh')
        self.win.refresh()


@click.command()
@click.option('-l', '--window', type=int, default=None,
              help='Display stats for a rolling window of data.')
@click.option('--debug', is_flag=True, help='Enable debug logging.')
def main(window=None, debug=False):
    """
    Live updating frequency distributions on streaming data. Like top, but
    for any line-by-line input. Pipe data in on stdin, and watch it be counted
    in real-time.
    """
    if debug:
        if os.path.exists('debug.log'):
            os.remove('debug.log')

        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    if window:
        err = curses.wrapper(anytop, n=window)
    else:
        err = curses.wrapper(anytop)

    if err:
        raise err
