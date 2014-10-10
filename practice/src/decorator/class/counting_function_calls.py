# -*- coding: utf-8 -*-

class countcalls(object):
    "Decorator that keeps track of the number of times a function is called."

    __instances = {}

    def __init__(self, f):
        print "__init__"
        self.__f = f
        self.__numcalls = 0
        countcalls.__instances[f] = self

    def __call__(self, *args, **kwargs):
        print "__call__"
        self.__numcalls += 1
        return self.__f(*args, **kwargs)

    @staticmethod
    def count(f):
        "Return the number of times the function f was called."
        return countcalls.__instances[f].__numcalls

    @staticmethod
    def counts():
        "Return a dict of {function: # of calls} for all registered functions."
        return dict([(f, countcalls.count(f)) for f in countcalls.__instances])

print 1
@countcalls
def test():
    print("test")

print 3
#__init__
@countcalls
def test2():
    print("test2")

print test
#__call__
test()
#__call__
test2()
print test.counts()