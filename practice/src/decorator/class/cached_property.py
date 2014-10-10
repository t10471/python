# -*- coding: utf-8 -*-

#
# © 2011 Christopher Arndt, MIT License
#
#引数ありクラスデコレータ
import time
import random


class cached_property(object):
    """Decorator for read-only properties evaluated only once within TTL period.

    It can be used to created a cached property like this::

        import random

        # the class containing the property must be a new-style class
        class MyClass(object):
            # create property whose value is cached for ten minutes
            @cached_property(ttl=600)
            def randint(self):
                # will only be evaluated every 10 min. at maximum.
                return random.randint(0, 100)

    The value is cached  in the '_cache' attribute of the object instance that
    has the property getter method wrapped by this decorator. The '_cache'
    attribute value is a dictionary which has a key for every property of the
    object which is wrapped by this decorator. Each entry in the cache is
    created only when the property is accessed for the first time and is a
    two-element tuple with the last computed property value and the last time
    it was updated in seconds since the epoch.

    The default time-to-live (TTL) is 300 seconds (5 minutes). Set the TTL to
    zero for the cached value to never expire.

    To expire a cached property value manually just do::

        del instance._cache[<property name>]

    """
    def __init__(self, ttl=300):
        print "__init__"
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        print "__call__"
        #print "fget"
        #print fget #function randint
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        print "__get__"
        now = time.time()
        try:
            value, last_update = inst._cache[self.__name__]
            if self.ttl > 0 and now - last_update > self.ttl:
                raise AttributeError
        except (KeyError, AttributeError):
            #print "inst"
            #print inst #MyClass object
            #print self #cached_property object
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}
            cache[self.__name__] = (value, now)
        return value

class MyClass(object):
    # create property whose value is cached for ten minutes
    #__init__
    #__call__
    @cached_property(ttl=600)
    def randint(self):
        print "randint"
        # will only be evaluated every 10 min. at maximum.
        return random.randint(0, 100)

print random.randint(0, 100)
my = MyClass()
#__get__
print my.randint
print my.randint
