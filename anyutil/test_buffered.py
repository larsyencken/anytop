# -*- coding: utf-8 -*-
#
#  test_buffered.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-27.
#  Copyright 2012 Lars Yencken. All rights reserved.
#

"""
Tests for buffered iteration support.
"""

import unittest

from buffered import BufferedIter as BI

class BufferedIterTest(unittest.TestCase):
    def test_iteration(self):
        lbi = lambda it: list(BI(it))
        self.assertEqual(lbi([]), [])
        self.assertEqual(lbi(xrange(3)), range(3))

    def test_peek(self):
        it = BI(xrange(4))
        assert not it.empty()
        self.assertEqual(it.peek(), 0)
        self.assertEqual(it.next(), 0)
        assert not it.empty()
        self.assertEqual(it.peek(), 1)
        self.assertEqual(it.next(), 1)
        assert not it.empty()
        self.assertEqual(it.peek(), 2)
        self.assertEqual(it.next(), 2)
        assert not it.empty()
        self.assertEqual(it.peek(), 3)
        self.assertEqual(it.next(), 3)
        assert it.empty()
        self.assertRaises(ValueError, it.peek)

    def test_dropwhile(self):
        it = BI(xrange(30))
        it.dropwhile(lambda x: x < 20)
        self.assertEqual(it.peek(), 20)
        self.assertEqual(list(it), range(20, 30))

    def test_takewhile(self):
        it = BI(xrange(30))
        self.assertEqual(list(it.takewhile(lambda x: x < 5)), [0, 1, 2, 3, 4])
        self.assertEqual(it.peek(), 5)
        self.assertEqual(list(it), range(5, 30))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(
            unittest.makeSuite(BufferedIterTest))
