# -*- coding: utf-8 -*-

from collections import defaultdict

class Singleton(type):
    def __new__(cls, name, bases, dict_):
        dict_['instance'] = None
        return type.__new__(cls, name, bases, dict_)

    def __call__(cls, *args): #@NoSelf
        if cls.instance == None:
            cls.instance = type.__call__(cls, *args)
            cls.__init__(cls.instance, *args)
        return cls.instance

class Session(defaultdict):
    __metaclass__=Singleton
    def __init__(self):
        super(Session, self).__init__(str)

Session()['a'] = 1
print Session()['a']
print Session()['a']

#print Session().a
#print Session().b