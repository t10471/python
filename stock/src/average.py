#!/user/bin/env python
# -*- coding: utf-8 -*

import re, datetime, urllib
import re, string
from  insert_table import dbManager
from create_talbe import Stock,DailyStock,Market,Business
from sqlalchemy import and_
import sys
from var_dump import var_dump
from pprint import pprint

def SMAverage(data, n):
    buff = []
    for x in xrange(len(data) - n ):
        y = 0.0
        for j in xrange(n):
            y += data[x + j][1]
        y /= n
        buff.append((data[x +  n ][0], y))
        
    return buff

#$B2C=EJ?6Q(B
def EMAverage(data, n):
    buff = []
    for x in xrange(len(data) - n ):
        #$B:G=i$N>l9g$@$1C1=c0\F0J?6Q$rA0F|$N(BEMA$B$H$9$k(B
        if(x == 0):
            y = 0.0
            for j in xrange(n):
                y += data[x + j][1]
            y /= n
                
        else :
            y = 0.0
            y = buff[x - 1][1]
        ema = data[x + n][1] * 2 / (n + 1) + y * (n + 1 - 2) / (n + 1)
        buff.append((data[x +  n ][0], ema))
         
    return buff
#RSI
def RSI(data, n):
    buff = []
    for x in xrange(len(data) - n ):
        #$B:G=i$N>l9g$@$1A0F|$NCM$,<hF@$G$-$J$$$N$G=hM}$7$J$$(B
        if x != 0 :
            ty = 0.0
            aty = 0.0
            y = 0.0
            for j in xrange(n):
                    y  = data[x + j][1] - data[x + j - 1][1]
                    if y > 0 :
                        ty += y
                    aty += abs(y)
            sri = (ty / aty) * 100
            buff.append((data[x +  n  ][0], sri))
         
    return buff
def ichimoku(data):
    nn = len(data)
    st = 25
    ct = 8
    a1 = 26
    a2 = 52
    st_o = []
    l_o = []
    a1_o = []
    a2_o = []
    ct_o = []
    date, price = datasplit(data)    
    for x in xrange(0,nn):
        if x < ct:
            st_o.append((data[x][0],None))
            l_o.append((data[x][0],None))
            a1_o.append((data[x][0],None))
            a2_o.append((data[x][0],None))
            ct_o.append((data[x][0], None))
            continue
        #$B4p=`@~(B
        print x
        if x > st:
            wk = 0
            max_d = max(price[(x - st):x])
            min_d = min(price[(x - st):x])
            wk = (max_d + min_d) / 2
            st_o.append((data[x][0], wk))
        else:
            st_o.append((data[x][0],None))
        #$BCY9T@~(B
        if x > a1:
            l_o.append((data[x]))
            #l_o[x - a1] = data[x]
        else:
            l_o.append((data[x][0],None))
        #$B@h9T%9%Q%s(B2
        if x > a2:
            max_d = max(price[(x - a2):x])
            min_d = min(price[(x - a2):x])
            wk = (max_d + min_d) / 2
            #a2_o[x + a1] = wk
            a2_o.append((data[x][0],wk))
        else:
            a2_o.append((data[x][0],None))

        #$BE>49@~(B
        max_d = max(price[(x - ct):x])
        min_d = min(price[(x - ct):x])
        wk = (max_d + min_d) / 2
        ct_o.append((data[x][0], wk))

        if x > st:
            wk = (st_o[x][1] + ct_o[x][1] ) / 2
            a1_o.append((data[x][0],wk))
        else:
            a1_o.append((data[x][0],None))
    #exit()
    return st_o, ct_o, l_o, a1_o, a2_o


def datasplit(data):
    date = []
    price = []
    for d in data:
        date.append(d[0])
        price.append(d[1])
    return date,price


