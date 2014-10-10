# -*- coding: utf-8 -*-

#ある処理を別のAPIの形式にあわせてラップする

from os.path import split, splitext

#fileのラップ
class DublinCoreAdaptar(object):
    def __init__(self, filename):
        self._filename = filename

    def titile(self):
        return splitext(split(self._filename)[-1])[0]

    def creator(self):
        return 'UNknown'

    def languages(self):
        return ('en',)
#使用者
class DublinCoreInfo(object):
    def summary(self, dc_ob):
        """
        @param dc_ob: DublinCoreAdaptar
        @type dc_ob: DublinCoreAdaptar
        """
        print 'Title: %s' % dc_ob.title()
        print 'Creator: %s' % dc_ob.creator()
        print 'Languagesr: %s' % ', '.join(dc_ob.languages())

adapted = DublinCoreAdaptar('exsample.txt')
infos = DublinCoreInfo()
print infos.summary(adapted)