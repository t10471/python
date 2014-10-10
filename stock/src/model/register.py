#*- coding: utf-8 -*-

from model.connection import get_session
from model.db import Stock, Market, Business

class Register(object):
    def __init__(self):
        self.sess = get_session()

    def RegisterStockBaseInfo(self):
        in_stock = self.sess.query(Stock).filter_by(code=self.s_code).first()
        if not in_stock:
            business = self.sess.query(Business).filter_by(name=self.job).first()
            #職業登録
            if not business:
                bobj = Business('',self.job,None)
                self.sess.add(bobj)
                self.sess.commit()
                biz = self.sess.query(Business).filter_by(name=self.job).first()
            else:
                biz = self.sess.query(Business).filter_by(name=self.job).first()
            #市場登録
            market = self.sess.query(Market).filter_by(code=self.m_code).first()
            if not market:
                mobj = Market(self.m_code, self.mark,None)
                self.sess.add(mobj)
            sobj = Stock(self.s_code, self.m_code, self.name, biz.business_code,None)
            self.sess.add(sobj)
            self.sess.commit()
