# -*- coding: utf-8 -*-
#
#  test_buffered.py
#  anytop
#

"""
Tests for buffered iteration support.
"""

import unittest

from anytop.buffer import buffered


class BufferedIterTest(unittest.TestCase):
    def test_iteration(self):
        self.assertSeqEqual(buffered([]), [])
        self.assertSeqEqual(buffered(range(3)), range(3))

    def assertSeqEqual(self, x, y):
        self.assertEqual(list(x), list(y))

    def test_peek(self):
        it = buffered(range(4))
        assert not it.empty()
        self.assertEqual(it.head, 0)
        self.assertEqual(next(it), 0)
        assert not it.empty()
        self.assertEqual(it.head, 1)
        self.assertEqual(next(it), 1)
        assert not it.empty()
        self.assertEqual(it.head, 2)
        self.assertEqual(next(it), 2)
        assert not it.empty()
        self.assertEqual(it.head, 3)
        self.assertEqual(next(it), 3)
        assert it.empty()
        assert it.head is None

    def test_dropwhile(self):
        it = buffered(range(30))
        it.dropwhile(lambda x: x < 20)
        self.assertEqual(it.head, 20)
        self.assertSeqEqual(it, range(20, 30))

    def test_takewhile(self):
        it = buffered(range(30))
        self.assertSeqEqual(it.takewhile(lambda x: x < 5), [0, 1, 2, 3, 4])
        self.assertEqual(it.head, 5)
        self.assertSeqEqual(it, range(5, 30))


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(
        unittest.makeSuite(BufferedIterTest)
    )
