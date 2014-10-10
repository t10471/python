# -*- coding: utf-8 -*-

import sys

WHAT_TO_DEBUG = set(['io', 'core'])  # change to what you need

class debug:
    """ Decorator which helps to control what aspects of a program to debug
    on per-function basis. Aspects are provided as list of arguments.
    It DOESN'T slowdown functions which aren't supposed to be debugged.
    """
    def __init__(self, aspects=None):
        print "__init__"
        self.aspects = set(aspects)

    def __call__(self, f):
        print "__call__"
        if self.aspects & WHAT_TO_DEBUG:
            def newf(*args, **kwds):
                #標準出力に出力
                print >> sys.stderr, f.func_name, args, kwds
                f_result = f(*args, **kwds)
                print >> sys.stderr, f.func_name, "returned", f_result
                return f_result
            newf.__doc__ = f.__doc__
            return newf
        else:
            return f

print 1
@debug(['io'])
def prn(x):
    print x

print 2
@debug(['core'])
def mult(x, y):
    return x * y

print 3
prn(mult(2, 2))