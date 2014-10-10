#!/user/bin/env python
# -*- coding: utf-8 -*-

import re, datetime, urllib
import mechanize
from BeautifulSoup import BeautifulSoup
#from html5lib import HTMLParser 
#from html5lib import treebuilders
from HTMLParser import HTMLParseError
import re, string
from  insert_table import dbManager
from create_talbe import Stock,DailyStock,Market,Business
from sqlalchemy import and_
import sys
import chardet


def main():
    """main(銘柄コード)"""
    d = datetime.datetime.today() 
    #今日の日付を取得
    date = str(d.year) + '/' + str(d.month) + '/' + str(d.day)
    manager = dbManager()
    sess = manager.get_sess()
    for stock in sess.query(Stock).order_by(Stock.stock_code.asc()):
        date_stock = ''
        date_stock = sess.query(DailyStock).filter(and_(DailyStock.stock_code==stock.stock_code , DailyStock.date==date))
        cnt =  date_stock.count()
        #今日のデータが存在するか？今日の分が存在したら処理しない
        if not cnt:
            #過去にデータを取得したことのある銘柄か?
            count_stock = ''
            count_stock = sess.query(DailyStock).filter('stock_code=:stock_code').params(stock_code=stock.stock_code)
            if count_stock.count() == 0:
                end_date = datetime.date.today()
                for cnt in range(1,10):
                    start_date = end_date - datetime.timedelta(days=50)
                    get_term_stock(stock.stock_code,stock.market_code,start_date,end_date,sess)
                    end_date = start_date -  datetime.timedelta(days=1)
            else:
                #過去に取得した銘柄なら今日の分のみ取得する
                end_date = datetime.date.today()
                start_date = datetime.date.today()
                get_term_stock(stock.stock_code,stock.market_code,start_date,end_date,sess)
def get_term_stock(code,market_code,start_ymd,end_ymd,sess):
    start_m, start_d, start_y = start_ymd.month, start_ymd.day, start_ymd.year # 開始月, 日, 年
    end_m, end_d, end_y = end_ymd.month, end_ymd.day, end_ymd.year  
    url_t = "http://table.yahoo.co.jp/t?s=%s.%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (code, market_code, start_m, start_d, start_y, end_m, end_d, end_y)
    enc = 'euc-jp'
    url_data = unicode(urllib.urlopen(url_t).read(), enc, 'ignore')
    parse_stock(code,url_data,sess)
    flg = 1 
def parse_stock(code,data,sess):
    soup = BeautifulSoup(data)
    soup.prettify()
    # 価格データを行を抽出し、リスト price_list に格納
    price_list = soup.findAll('tr',align="right",bgcolor="#ffffff")
    # 日付ごとにタブ区切りで書き出し
    for data in price_list:
        date_str = data.contents[1].small.string
        # 日付文字列修正 yyyy年m月d日 -> yyyy/m/d
        date_str = re.sub(u"日", u"", re.sub(u"[年月]", u"-", date_str))
        start_p = data.contents[3].small.string
        start_p = re.sub(u",", u"",  start_p)
        max_p = data.contents[5].small.string
        max_p = re.sub(u",", u"",  max_p)
        min_p = data.contents[7].small.string
        min_p = re.sub(u",", u"",  min_p)
        end_p = data.contents[9].b.string
        end_p = re.sub(u",", u"",  end_p)
        vol = data.contents[11].small.string
        vol = re.sub(u",", u"",  vol)
        print "%s,%s,%s,%s,%s,%s,%s" % (code,date_str,start_p,max_p,min_p,end_p,vol)
        dobj = DailyStock(code,date_str,start_p,max_p,min_p,end_p,vol,None)
        sess.add(dobj)
        sess.commit()
if __name__ == "__main__":
    main()


