# -*- coding: utf-8 -*-

'''
Created on 2011/11/18

@author: tn10
'''
import functools

class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        print 'init'
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        print '__call__'
        #メソッドの場合、argsはもとのオブジェクトと引数
        #関数の場合、引数
        print args
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    def __get__(self, obj, objtype):
        """Support instance methods."""
        print '__get__'
        #print obj #-> _main__.Test object
        #print objtype #-> class '__main__.Test'

        #objのself.__call__のメソッドを返す
        #objはもとのオブジェクト
        #型はfunctools.partialオブジェクト
        return functools.partial(self.__call__, obj)

@memoized
def fibonacci(n):
    "Return the nth fibonacci number."
    if n in (0, 1):
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

#関数に適用した場合、__get__は呼ばれず__call__のみ呼ばれる
#print fibonacci(12)

class Test(object):
    def __init__(self, arg):
        print "Test __init__"
        self.arg = arg
    #__init__
    @memoized
    def cul(self, n):
        print 'cul method'
        return n * self.arg

print "start"
test = Test(10)
print "cul 2"
#呼ばれる順
#__get__
#__call__
#cul
test.cul(2)
#print "cul 2"
#test.cul(2)
#print "cul 3"
#test.cul(3)
