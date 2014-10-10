# -*- coding: utf-8 -*-

class curried(object):
    """
    Decorator that returns a function that keeps returning functions
    until all arguments are supplied; then the original function is
    evaluated.
    """

    def __init__(self, func, *a):
        print "__init__"
        print a
        self.func = func
        self.args = a
    def __call__(self, *a):
        print "__call__"
        print a
        args = self.args + a
        #print self.func.func_code
        #code object add
        #co_argcountは引数の数
        if len(args) < self.func.func_code.co_argcount:
            return curried(self.func, *args)
        else:
            return self.func(*args)


@curried
def add(a, b):
    print "add"
    return a + b
@curried
def add2(a, b, c):
    print "add"
    print a,b,c
    return a + b + c

print "1"
add1 = add(1)

print "2"
print add1(2)

print "1"
add21 = add2(1)
print "2"
add22 = add21(2)
print "3"
print add22(3)
