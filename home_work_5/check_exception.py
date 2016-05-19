#! /usr/bin/env python3
import sys


class AssertRaises(object):

    def __init__(self, exception_type):
        self.exception_type = exception_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None or not issubclass(exc_type, self.exception_type):
            raise AssertionError
        else:
            return True

exec(sys.stdin.read())
