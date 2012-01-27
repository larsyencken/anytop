# -*- coding: utf-8 -*-
#
#  test_accumulate.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-27.
#  Copyright 2012 Lars Yencken. All rights reserved.
#

"""
Tests for the accumulate module.
"""

import unittest

import accumulate
import random

class FloatRangeTestCase(unittest.TestCase):
    def test_range(self):
        r = accumulate.FloatRange(0, 2, 2)
        self.assertEqual(list(r), [(0.0, 1.0), (1.0, 2.0)])
        self.assertEqual(len(r), 2)

    def test_get_bin(self):
        r = accumulate.FloatRange(0, 2, 2)
        self.assertEqual(r.get_bin(-0.1), None)
        self.assertEqual(r.get_bin(0.0), (0.0, 1.0))
        self.assertEqual(r.get_bin(0.00001), (0.0, 1.0))
        self.assertEqual(r.get_bin(0.99999), (0.0, 1.0))
        self.assertEqual(r.get_bin(1.0), (1.0, 2.0))
        self.assertEqual(r.get_bin(1.00001), (1.0, 2.0))
        self.assertEqual(r.get_bin(1.99999), (1.0, 2.0))
        self.assertEqual(r.get_bin(2.0), None)
        self.assertEqual(r.get_bin(2.1), None)

    def test_get_bin_2(self):
        frange = accumulate.FloatRange(1, 7, 6)
        self.assertEqual(list(frange), [
            (1.0, 2.0),
            (2.0, 3.0),
            (3.0, 4.0),
            (4.0, 5.0),
            (5.0, 6.0),
            (6.0, 7.0),
        ])
        self.assertEqual(frange.get_bin(0), None)
        self.assertEqual(frange.get_bin(1), (1.0, 2.0))
        self.assertEqual(frange.get_bin(2), (2.0, 3.0))
        self.assertEqual(frange.get_bin(3), (3.0, 4.0))
        self.assertEqual(frange.get_bin(4), (4.0, 5.0))
        self.assertEqual(frange.get_bin(5), (5.0, 6.0))
        self.assertEqual(frange.get_bin(6), (6.0, 7.0))
        self.assertEqual(frange.get_bin(7), None)

class NumericAccumulatorTestCase(unittest.TestCase):
    def test_dist(self):
        data = [0, 1, 1, 2, 3, 3, 3, 4, 6, 6, 6, 7, 7, 8]
        random.shuffle(data)
        frange = accumulate.FloatRange(1, 7, 6)
        assert frange.end == 7.0
        self.assertEqual(frange.get_bin(6), (6.0, 7.0))
        acc = accumulate.NumericAccumulator()
        acc.consume_all(data)
        self.assertEqual(acc, sorted(data))
        dist = acc.get_dist(frange)
        expected_dist = {
                None:       4,
                (1.0, 2.0): 2,
                (2.0, 3.0): 1,
                (3.0, 4.0): 3,
                (4.0, 5.0): 1,
                (5.0, 6.0): 0,
                (6.0, 7.0): 3,
            }
        for k in expected_dist:
            self.assertEqual(dist[k], expected_dist[k])

        assert set(dist).issubset(set(expected_dist))

class AccumulatorTestCase(unittest.TestCase):
    def test_basic(self):
        data = ['a', 'a', 'b', 'c', 'a']
        acc = accumulate.Accumulator()
        for x in data:
            acc.consume(x)

        expected_dist = {'a': 3, 'b': 1, 'c': 1}
        dist = acc.to_dist()
        for k in expected_dist:
            self.assertEqual(dist[k], expected_dist[k])
        assert set(dist).issubset(expected_dist)

class WindowAccumulatorTestCase(unittest.TestCase):
    def test_basic(self):
        acc = accumulate.WindowAccumulator(3)
        for x in ['a', 'a', 'b']:
            acc.consume(x)
        dist = acc.to_dist()
        self.assertEqual(dist['a'], 2)
        self.assertEqual(dist['b'], 1)

        acc.consume('c')
        acc.consume('b')
        dist = acc.to_dist()
        self.assertEqual(dist['b'], 2)
        self.assertEqual(dist['c'], 1)

def suite():
    return unittest.TestSuite((
            unittest.makeSuite(FloatRangeTestCase),
            unittest.makeSuite(NumericAccumulatorTestCase),
        ))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())

