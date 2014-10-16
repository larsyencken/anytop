#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  anyhist.py
#  anytop
#

"""
Display a command-line histogram.
"""

import os
import sys
import threading
import logging
import time
import curses

import click

from anytop import (
    common,
    accumulate
)

BORDER_PADDING = 0.03


def anyhist(win, istream=sys.stdin, n=None):
    "Visualize the incoming numbers by their distribution."
    common.init_win(win)
    if n:
        raise ValueError('fixed window size not yet supported')
    else:
        accumulator = accumulate.NumericAccumulator()
    lock = threading.Lock()
    logging.debug('Starting UI thread')
    ui = AnyHistUI(win, lock, accumulator)
    ui.start()

    try:
        for line in common.robust_line_iter(istream):
            x = float(line)
            logging.debug('INPUT: %f' % x)

            if ui.error:
                return ui.error

            logging.debug('INPUT: requesting lock')
            lock.acquire()
            logging.debug('INPUT: lock acquired')
            accumulator.consume(x)
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

    except Exception as e:
        return e

    finally:
        ui.stop()
        ui.join()

    return ui.error


class AnyHistUI(threading.Thread):
    def __init__(self, win, lock, accumulator):
        self.win = win
        self.acc = accumulator
        self.lock = lock
        self.error = None
        self._stop_event = threading.Event()
        super(AnyHistUI, self).__init__()

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
                self.refresh_display(self.acc)
                self.lock.release()
                logging.debug('UI: lock released')

                time.sleep(1)
        except Exception as e:
            self.lock.release()
            self.error = e
            return

    def refresh_display(self, acc):
        "Redraw the screen with the current data."
        logging.debug('UI: refreshing the display')
        self.win.erase()
        height, width = self.win.getmaxyx()
        logging.debug('UI: size is %d x %d' % (width, height))

        n = len(acc)

        logging.debug('UI: redraw call')
        self.win.redrawwin()

        if n < 2:
            logging.debug('UI: refresh')
            self.win.addstr(0, 0, 'waiting for data...')
            self.win.refresh()
            return

        min_ = min(acc)
        max_ = max(acc)

        # go a few % out either side for padding
        diff = max_ - min_
        min_ -= BORDER_PADDING * diff
        max_ += BORDER_PADDING * diff

        frange = accumulate.FloatRange(min_, max_, height - 2)
        dist = acc.get_dist(frange)
        labels = [('%g' % r[1]) for r in frange]

        max_label = max(map(len, labels))
        hist_width = width - max_label - 3

        largest = max(dist.itervalues())
        zoom = common.get_zoom(largest, hist_width)
        logging.debug('UI: using zoom %d' % zoom)

        self.win.addstr(0, 0, '%d values, 1/%d zoom' % (n, zoom))

        template = '%%-%dg  %%s' % max_label
        for i, (start, end) in enumerate(frange):
            l = template % (end, '#'*(dist[(start, end)] / zoom))
            self.win.addstr(i + 2, 0, l)

        logging.debug('UI: refresh')
        self.win.refresh()


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging.')
def main(debug=False):
    "Reads numbers from stdin and displays a frequency histogram of them."
    if debug:
        if os.path.exists('debug.log'):
            os.remove('debug.log')

        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    try:
        err = curses.wrapper(anyhist)
        if err:
            raise err

    except KeyboardInterrupt:
        pass
