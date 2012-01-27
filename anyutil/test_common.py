# -*- coding: utf-8 -*-
#
#  test_common.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-27.
#  Copyright 2012 Lars Yencken. All rights reserved.
#

"""
Tests for the common utilities.
"""

import unittest

import common

class ZoomTestCase(unittest.TestCase):
    def test_zoom(self):
        self.assertEqual(common.get_zoom(0, 100), 1)
        self.assertEqual(common.get_zoom(99, 100), 1)
        self.assertEqual(common.get_zoom(100, 100), 1)
        self.assertEqual(common.get_zoom(101, 100), 2)
        self.assertEqual(common.get_zoom(201, 100), 2)
        self.assertEqual(common.get_zoom(202, 100), 3)
        self.assertEqual(common.get_zoom(303, 100), 5)
        self.assertEqual(common.get_zoom(505, 100), 10)
        self.assertEqual(common.get_zoom(1010, 100), 20)

def suite():
    return unittest.TestSuite((
            unittest.makeSuite(ZoomTestCase),
        ))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())

