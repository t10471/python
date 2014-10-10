# -*- coding: utf-8 -*-

#戦略を分ける

import os
import time
from decimal import Decimal
import csv

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

#Strategyに相当する
class ReadItemDataStrategy(object):

    def __init__(self, filename):
        self.filename = filename

    #データファイルを読み込み、オブジェクトの配列で返す
    #Contextに提供するメソッド
    #@param string データファイル名
    #@return データオブジェクトの配列
    def getData(self):
        if os.access(self.filename, os.R_OK) == False:
            raise Exception, 'file [' + self.getFilename() + '] is not readable !'

        return self.readData(self.getFilename())

    #ファイル名を返す
    #@return ファイル名
    def getFilename(self):
        return self.filename


#固定長データを読み込む
#ConcreteStrategyに相当する
class ReadFixedLengthDataStrategy(ReadItemDataStrategy):


    #データファイルを読み込み、オブジェクトの配列で返す
    #@param string データファイル名
    #@return データオブジェクトの配列
    def readData(self, filename):
        return_value = []
        with file(filename) as lines:
            reader = csv.reader(lines)
            try:
                next(lines)
            except Exception as e:
                return return_value
            for line in reader:
                item_name = line[0]
                item_code = line[1]
                price = int(line[2])
                release_date = line[3]

                #戻り値のオブジェクトの作成
                obj = type('lamdbaobject', (object,), {})()
                obj.item_name = item_name
                obj.item_code = item_code
                obj.price = price
                obj.release_date = time.strptime(release_date, '%Y%m%d')
                return_value.append(obj)
        return return_value

class ReadTabSeparatedDataStrategy(ReadItemDataStrategy):


    #データファイルを読み込み、オブジェクトの配列で返す
    #@param string データファイル名
    #@return データオブジェクトの配列

    def readData(self, filename):
        return_value = []
        with file(filename) as lines:
            try:
                next(lines)
            except Exception as e:
                return return_value
            for line in lines:
                item_list = line.split('\t')

                #戻り値のオブジェクトの作成
                obj = type('lamdbaobject', (object,), {})()
                obj.item_code = item_list.pop(0)
                obj.item_name = item_list.pop(0)
                obj.price = int(item_list.pop(0))
                obj.release_date = time.strptime(item_list.pop(0).strip(), '%Y/%m/%d')
                return_value.append(obj)
        return return_value


#Contextに相当する
class ItemDataContext(object):

    #コンストラクタ
    #@param ReadItemDataStrategy ReadItemDataStrategyオブジェクト
    def __init__(self, strategy):
        self.strategy = strategy

    #商品情報をオブジェクトの配列で返す
    #@return データオブジェクトの配列
    def getItemData(self):
        return self.strategy.getData()

def dumpData(data):
    for object in data:
        print '商品番号：' + object.item_code
        print '\\' + moneyfmt(Decimal(object.price), 0, dp="") + '-'
        print time.strftime('%Y/%m/%d', object.release_date) + '発売'


if __name__ == "__main__":


    #固定長データを読み込む

    strategy1 = ReadFixedLengthDataStrategy('fixed_length_data.txt')
    context1 = ItemDataContext(strategy1)
    dumpData(context1.getItemData())

    #タブ区切りデータを読み込む
    strategy2 = ReadTabSeparatedDataStrategy('tab_separated_data.txt')
    context2 = ItemDataContext(strategy2)
    dumpData(context2.getItemData())