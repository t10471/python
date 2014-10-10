# -*- coding: utf-8 -*-

#インスタンスをコピーして作成する

from decimal import Decimal
from copy import copy, deepcopy

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


class ItemPrototype(object):
    def __init__(self, code, name, price):
        self.item_code = code
        self.item_name = name
        self.price = price

    def getCode(self):
        return self.item_code

    def getName(self):
        return self.item_name

    def getPrice(self):
        return self.price

    def setDetail(self, detail):
        self.detail = detail

    def getDetail(self):
        return self.detail

    def dumpData(self):
        print self.getName()
        print '商品番号' + self.getCode()
        print '\\' + moneyfmt(Decimal(self.getPrice()), 0, dp="") + '-'
        print self.detail.comment

    #cloneキーワードを使って新しいインスタンスを作成する
    def newInstance(self):
        new_instance = self._clone(self)
        return new_instance

class DeepCopyItem(ItemPrototype):

    #深いコピーを行うための実装
    #内部で保持しているオブジェクトもコピー
    def _clone(self, obj):
        return deepcopy(obj)

class ShallowCopyItem(ItemPrototype):

    #浅いコピーを行うので、空の実装を行う
    def _clone(self, obj):
        return copy(obj)

class ItemManager:

    def __init__(self):
        self.items = {}


    def registItem(self, item):
        self.items[item.getCode()] = item

    #Prototypeクラスのメソッドを使って、新しいインスタンスを作成
    def create(self, item_code):
        if item_code not in  self.items:
            raise Exception, 'item_code [' + item_code + '] not exists !'

        cloned_item = self.items[item_code].newInstance()

        return cloned_item

def testCopy(manager, item_code):

    #商品のインスタンスを2つ作成
    item1 = manager.create(item_code)
    item2 = manager.create(item_code)

    #1つだけコメントを削除
    item2.getDetail().comment = 'コメントを書き換えました'

    #商品情報を表示
    #深いコピーをした場合、item2への変更はitem1に影響しない
    print '■オリジナル'
    item1.dumpData()
    print '■コピー'
    item2.dumpData()


if __name__ == "__main__":
    manager = ItemManager()
    #商品データを登録
    item = DeepCopyItem('ABC0001', '限定Ｔシャツ', 3800)
    detail = type('lamdbaobject', (object,), {})()
    detail.comment = '商品Aのコメントです'
    item.setDetail(detail)
    manager.registItem(item)

    item = ShallowCopyItem('ABC0002', 'ぬいぐるみ', 1500)
    detail = type('lamdbaobject', (object,), {})()
    detail.comment = '商品Bのコメントです'
    item.setDetail(detail)
    manager.registItem(item)

    testCopy(manager, 'ABC0001')
    testCopy(manager, 'ABC0002')