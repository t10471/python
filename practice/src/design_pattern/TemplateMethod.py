# -*- coding: utf-8 -*-

#単なる継承

class Base(object):
    def __init__(self):
        pass
    def meth(self, int):
        return self._meth(int)

    def _meth(self, int):
        return int

class Pow(Base):
    def _meth(self, int):
        return pow(int,int)
