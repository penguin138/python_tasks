#! /usr/bin/env python3
import sys


def unique(iterable):
    iterator = iter(iterable)
    prev = None
    try:
        while True:
            current = next(iterator)
            if current != prev:
                yield current
            prev = current
    except StopIteration:
        pass

exec(sys.stdin.read())
