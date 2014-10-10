#!/user/bin/env python
# -*- coding: utf-8 -*-

import re, datetime, urllib
import mechanize
import re, string
from  insert_table import dbManager
from create_talbe import Stock,DailyStock,Market,Business
from sqlalchemy import and_
import sys
from pprint import pprint
from average import *
#class A(object):
#    def __init__(self, num):
#        self.num = num

def main():
    """main(銘柄コード)"""
    #a = A(5)
    #a.list = [A(3), A(4)]
    #a.dict = {"x": [A(3), A(5)], A(100): 100}
    #a.set = set([A(5), 100])
    #var_dump(a)

    manager = dbManager()
    sess = manager.get_sess()
    for stock in sess.query(Stock).order_by(Stock.stock_code.asc()):
        date_stock = None
        date_stock = sess.query(DailyStock).filter(DailyStock.stock_code==stock.stock_code).order_by(DailyStock.date.asc())
        data = [(stock.date,float(stock.end_price)) for stock in date_stock]
        print stock.stock_code
        #out1 = SMAverage(data,20)
        #pprint(out1[0])
        #out2 = EMAverage(data,20)
        #pprint(out2)
        #out3 = RSI(data,14)
        #pprint(out3)
        st, ct, l, a1, a2 = ichimoku(data)
        print "st"
        pprint(st)
        print "ct"
        pprint(ct)
        print "l"
        pprint(l)
        print "a1"
        pprint(a1)
        print "a2"
        pprint(a2)
        sys.exit()
if __name__ == "__main__":
    main()


