import path
path.dummy()
import t10471.yahoo.finance.stock.daily.html.getter as getter
import t10471.yahoo.finance.stock.daily.html.parser as parser
import t10471.model.register as register
import datetime


class Daily(object):

    def __init__(self):
        url = 'http://info.finance.yahoo.co.jp/history/?code=%s.%s&sy=%s&sm=%s&sd=%s&ey=%s&em=%s&ed=%s&tm=d'
        self.getter = getter.HtmlGetter(url)
        self.register = register.Register()
        self.parser = parser.HtmlParser(self.register)
        self.today = datetime.datetime.today()

    def run(self):
        today = self.today.strftime("%Y/%m/%d")
        for stock in self.register.getStocks():
            print(stock)
            stock_data = self.register.getTodayStockDate(stock, today)
            if stock_data.count() > 0:
                continue
            delta = 0
            if not self.register.countSotckData(stock):
                delta = 150
            for soup in self.getter.get(stock, self.today, delta):
                self.parser.setStock(stock)
                for rg in self.parser.parse(soup):
                    rg.registerStockDate()
        self.register.commit()

if __name__ == '__main__':
    Daily().run()
