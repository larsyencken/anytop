# -*- coding: utf-8 -*-
#
#  accumulate.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-27.
#  Copyright 2012 Lars Yencken. All rights reserved.
#

"""
Accumulate input into a useful summary.
"""

from collections import defaultdict, deque
import bisect
import itertools

class FloatRange(object):
    "A floating point range representing frequency bins."
    def __init__(self, start, end, n):
        self.start = float(start)
        self.end = float(end)
        self.n = n
        self.interval = (self.end - self.start) / float(n)
        self.bin_markers = self._gen_bins()

    def _gen_bins(self):
        bins = [self.start]
        for i in xrange(1, self.n + 1):
            bins.append(self.start + i * self.interval)
        assert abs(bins[-1] - self.end) < 1e-6
        return bins
    
    def __iter__(self):
        for i in xrange(self.n):
            yield (self.bin_markers[i], self.bin_markers[i+1])
    
    def __len__(self):
        return self.n
    
    def get_bin(self, x, default=None):
        i = bisect.bisect(self.bin_markers, x)
        if i == 0:
            return default
        if i == len(self.bin_markers):
            return default
        return (self.bin_markers[i-1], self.bin_markers[i])

class NumericAccumulator(list):
    def consume(self, x):
        bisect.insort(self, x)

    def consume_all(self, xs):
        for x in xs:
            self.consume(x)

    def get_dist(self, frange):
        """
        Given a start point, and then the end points of n sequential buckets,
        return a mapping from bucket index to counts.
        """
        dist = defaultdict(int)
        for bucket_index, xs in itertools.groupby(self, key=frange.get_bin):
            xs = list(xs)
            count = sum(1 for x in xs)
            dist[bucket_index] += count

        return dist

class Accumulator(defaultdict):
    "Accumulate counts without end."
    def __init__(self):
        super(Accumulator, self).__init__(int)

    def consume(self, key):
        self[key] += 1

    def to_dist(self):
        return self

class WindowAccumulator(deque):
    "Accumulate counts within a fixed-size rolling window."
    def __init__(self, n):
        super(WindowAccumulator, self).__init__([], n)

    def consume(self, key):
        self.append(key)

    def to_dist(self):
        d = defaultdict(int)
        for t in self:
            d[t] += 1
        return d

