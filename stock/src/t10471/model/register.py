from t10471.model.connection import get_session
from t10471.model.db import Stock, Market, Business, StockDate
from sqlalchemy import and_

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

    def getStocks(self):
        return self.sess.query(Stock).order_by(Stock.code)

    def getTodayStockDate(self, stock, date):
        return self.sess.query(StockDate).filter(and_(StockDate.stock_code == stock.code, StockDate.date == date))

    def countSotckData(self, stock):
        return self.sess.query(StockDate).filter(StockDate.stock_code == stock.code).count()

    def setStockDate(self, stock_code, date, start_price, max_price, min_price, end_price, volume):
        self.stock_date = StockDate(stock_code, date, start_price, max_price, min_price, end_price, volume, None)
        print(self.stock_date)

    def clearStockDate(self):
        self.stock_date = None

    def registerStockDate(self):
        if self.stock_date is None:
            return
        self.sess.add(self.stock_date)

    def commit(self):
        self.sess.commit()
