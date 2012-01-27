# -*- coding: utf-8 -*-
#
#  buffer.py
#  anytop
#
#  Created by Lars Yencken on 2012-01-27.
#  Copyright 2012 99designs. All rights reserved.
#

"""
Buffered iteration support.
"""

class BufferedIter(object):
    def __init__(self, it):
        self.it = iter(it)
        self._head = None
        self._empty = False

        self._advance()

    def __iter__(self):
        return self

    def next(self):
        if self._empty:
            raise StopIteration

        head = self._head
        self._advance()
        return head
    
    def empty(self):
        return self._empty

    def peek(self):
        if self._empty:
            raise ValueError

        return self._head

    def _advance(self):
        try:
            self._head = self.it.next()
        except StopIteration:
            self._empty = True

    def dropwhile(self, predicate):
        "Drop a prefix that matches the given predicate."
        while not self.empty() and predicate(self._head):
            self._advance()

    def takewhile(self, predicate):
        while not self.empty() and predicate(self._head):
            yield self.peek()
            self._advance()


