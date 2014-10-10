# -*- coding: utf-8 -*-

from functools import wraps
import sys
import random

def decorate(f):
    '''
    Class method decorator specific to the instance.

    It uses a descriptor to delay the definition of the
    method wrapper.
    '''
    class descript(object):
        def __init__(self, f):
            print self.__class__, sys._getframe().f_code.co_name
            self.f = f

        def __get__(self, instance, klass):
            print self.__class__, sys._getframe().f_code.co_name, instance, klass
            if instance is None:
                # Class method was requested
                return self.make_unbound(klass)
            return self.make_bound(instance)

        def make_unbound(self, klass):
            @wraps(self.f)
            def wrapper(*args, **kwargs):
                '''This documentation will vanish :)'''
                raise TypeError(
                    'unbound method %s() must be called with %s instance '
                    'as first argument (got nothing instead)'
                    %
                    (self.f.__name__, klass.__name__)
                )
            return wrapper

        def make_bound(self, instance):
            @wraps(self.f)
            def wrapper(*args, **kwargs):
                '''This documentation will disapear :)'''
                print "Called the decorated method %r of %r"%(self.f.__name__, instance)
                return self.f(instance, *args, **kwargs)
            # This instance does not need the descriptor anymore,
            # let it find the wrapper directly next time:
            setattr(instance, self.f.__name__, wrapper)
            return wrapper

    return descript(f)


class MyClass(object):
    #__init__
    @decorate
    def randint(self):
        print "randint"
        return random.randint(0, 100)


#print "my"
my = MyClass()
print my.randint()
