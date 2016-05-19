#! /usr/bin/env python3
import sys
from functools import wraps


def takes(*types):
    def check_types(function):
        @wraps(function)
        def new_function(*args):
            args_n_types = zip(args, types)
            for arg, type_ in args_n_types:
                if not isinstance(arg, type_):
                    raise TypeError("{} is not instance of {}".format(arg, type_))
            return function(*args)
        return new_function
    return check_types

exec(sys.stdin.read())
