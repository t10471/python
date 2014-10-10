# -*- coding: utf-8 -*-

import functools

def singleton(cls):
    """ Use class as singleton. """
    print cls
    print cls.__new__

    cls.__new_original__ = cls.__new__

    #cls.__new__をラップするためにfunctools.wrapsをおこなう
    @classmethod
    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        print "singleton_new"
        it =  cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        print "it", it
        it.__init_original__(*args, **kw)
        return it

    print 1
    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    print singleton_new
    print cls.__new__

    print 2
    return cls

#
# Sample use:
#
#Foo にはメタクラスで実装された __call__ というメソッドがあり、
#Foo()を実行するとは、この __call__ を実行することだ。
#
#__call__ の内部は、始めに Foo の __new__ を実行する。
#(今回は object で実装された __new__ を実行する)
#__new__ は Python の object を作成し、返す。(return する)
#
#次に、__call__ は __new__ で返された object の __init__ を実行する。
#(今回は object で実装された __init__ を実行する。
#実質的に何もしない)

@singleton
#class Foo:
class Foo(object):

    @classmethod
    def __new__(cls, *args, **kw):
        print "cls", cls
        cls.x = 10
        return object.__new__(cls)

    def __init__(self, *args, **kw):
        print "self", self
        assert self.x == 10
        self.x = 15

assert Foo().x == 15
Foo().x = 20
assert Foo().x == 20