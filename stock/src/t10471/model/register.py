from t10471.model.connection import get_session
from t10471.model.db import Stock, Market, Business

class Register(object):

    def __init__(self):
        self.sess = get_session()

    def RegisterStock(self):
        stock = self.sess.query(Stock).filter_by(code=self.stock.code).first()
        if not stock:
            self.sess.add(self.stock)
            self.sess.flush()

    def setMarket(self, code, name):
        market = self.sess.query(Market).filter_by(code=code).first()
        if not market:
            self.market = Market(code, name, None)
            self.sess.add(self.market)
            self.sess.flush()
        else:
            self.market = market

    def setBusiness(self, code, name):
        business = self.sess.query(Business).filter_by(name=name).first()
        if not business:
            self.business = Business('', name, None)
            self.sess.add(self.business)
            self.sess.flush()
            self.business = self.sess.query(Business).filter_by(name=name).first()
            print(self.business)
        else:
            self.business = business

    def setStock(self, code, market_code, name, business_code):
        self.stock = Stock(code, market_code, name, business_code, None)

    def getBusinessCode(self):
        return self.business.code

    def commit(self):
        self.sess.commit()
