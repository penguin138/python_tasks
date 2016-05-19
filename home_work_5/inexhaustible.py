#! /usr/bin/env python3
import sys
from functools import wraps


class InexhaustibleGenerator(object):

    def __init__(self, generator, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.generator = generator

    def __iter__(self):
        return iter(self.generator(*self.args, **self.kwargs))


def inexhaustible(generator):
    @wraps(generator)
    def decorated_generator(*args, **kwargs):
        return InexhaustibleGenerator(generator, *args, **kwargs)
    return decorated_generator


# just for me:
# new_generator = inexaustible(generator)(args, kwargs) -> iter(new_generator) = new_object

exec(sys.stdin.read())
