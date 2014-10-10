# -*- coding: utf-8 -*-

import sys

#関数パラメーター property(fget=None, fset=None, fdel=None, doc=None)
#
#　　　　fget　プロパティを取得するメソッド名
#　　　　fset　プロパティを設定するメソッド名
#　　　　fdel　プロパティを削除するメソッド名
#　　　　doc　　プロパティの説明文

def propget(func):
    locals = sys._getframe(1).f_locals #@ReservedAssignment
    print sys._getframe(1)
    print locals
    name = func.__name__
    prop = locals.get(name)
    if not isinstance(prop, property):
        prop = property(func, doc=func.__doc__)
    else:
        doc = prop.__doc__ or func.__doc__
        prop = property(func, prop.fset, prop.fdel, doc)
    return prop

def propset(func):
    locals = sys._getframe(1).f_locals #@ReservedAssignment
    name = func.__name__
    prop = locals.get(name)
    if not isinstance(prop, property):
        prop = property(None, func, doc=func.__doc__)
    else:
        doc = prop.__doc__ or func.__doc__
        prop = property(prop.fget, func, prop.fdel, doc)
    return prop

def propdel(func):
    locals = sys._getframe(1).f_locals #@ReservedAssignment
    name = func.__name__
    prop = locals.get(name)
    if not isinstance(prop, property):
        prop = property(None, None, func, doc=func.__doc__)
    else:
        prop = property(prop.fget, prop.fset, func, prop.__doc__)
    return prop

# These can be used like this:

class Example(object):

    def __init__(self, halt):
        self._half = halt

    @propget
    def myattr(self):
        return self._half * 2

    @propset
    def myattr(self, value): #@DuplicatedSignature
        self._half = value / 2

    @propdel
    def myattr(self): #@DuplicatedSignature
        del self._half

ex = Example(2)
print ex.myattr
ex.myattr = 3
print ex.myattr
print locals()
