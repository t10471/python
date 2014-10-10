# -*- coding: utf-8 -*-
from decimal import *

#キャッシュ

class Item(object):
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def getCode(self):
        return self.code

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price


class ItemFactory(object):
    instance = None
    def __init__(self, filename):
        self.buildPool(filename)

    @classmethod
    def getInstance(cls, filename):
        if cls.instance is None:
            cls.instance = ItemFactory(filename)
        return cls.instance

    def getItem(self, code):
        if code in self.pool:
            return self.pool[code]
        else:
            return None
    def buildPool(self, fname):
        self.pool = {}
        with open(fname, "r") as f:
            for line in f:
                item_code, item_name, price = line.split(',')
                self.pool[item_code] = Item(item_code, item_name, price)



def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Decimal を通貨表現の文字列に変換します。

    places:  小数点以下の値を表すのに必要な桁数
    curr:    符号の前に置く通貨記号 (オプションで、空でもかまいません)
    sep:     桁のグループ化に使う記号、オプションです (コンマ、ピリオド、
             スペース、または空)
    dp:      小数点 (コンマまたはピリオド)
             小数部がゼロの場合には空にできます。
    pos:     正数の符号オプション: '+', 空白または空文字列
    neg:     負数の符号オプション: '-', '(', 空白または空文字列
    trailneg:後置マイナス符号オプション:  '-', ')', 空白または空文字列

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='')
    '-1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='', neg='(', trailneg=')')
    '(1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places -. '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))

def dumpData(data):
    for obj in data:
        print obj.getName()
        print u'商品番号: ' + obj.getCode()
        print u'\\' +  moneyfmt(Decimal(obj.getPrice()), 0, dp="")

if __name__ == '__main__':

    factory = ItemFactory.getInstance('data.txt')
    items = []
    items.append(factory.getItem('ABC0001'))
    items.append(factory.getItem('ABC0002'))
    items.append(factory.getItem('ABC0003'))

    dumpData(items)

    if items[0] == factory.getItem('ABC0001'):
        print '同一のオブジェクトです'
    else:
        print '同一のオブジェクトではありません'
