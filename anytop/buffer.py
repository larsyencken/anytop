# -*- coding: utf-8 -*-
#
#  buffer.py
#  anytop
#

"""
Buffered iteration support.
"""


class buffered(object):
    def __init__(self, it):
        self.tail = iter(it)
        self.head = self._advance()

    def __iter__(self):
        return self

    def __next__(self):
        v = self.head
        if v is None:
            raise StopIteration

        self.head = self._advance()
        return v

    # for python 2.7
    next = __next__

    def _advance(self):
        try:
            return next(self.tail)
        except StopIteration:
            pass

    def empty(self):
        return self.head is None

    def dropwhile(self, f):
        "Drop a prefix that matches the given predicate."
        while not self.empty() and f(self.head):
            self.head = self._advance()

    def takewhile(self, f):
        "Return an interator over the prefix matching the predicate."
        while not self.empty() and f(self.head):
            v = self.head
            self.head = self._advance()
            yield v
