import t10471.html.parser as hparser
import mechanicalsoup

class HtmlParser(hparser.HtmlParser):

    def __init__(self, register):
        super(HtmlParser, self).__init__()
        self.register = register
        self.br = mechanicalsoup.Browser(soup_config={'features':'html.parser'})

    def parse(self, soup):
        self.register.clearStockDate()
        # 株式分割などイレギュラーな形式が存在
        try:
            tds =  soup.find_all('td')
            date = tds[0].string.replace('年','/').replace('月','/').replace('日','')
            start_price = tds[1].string.replace(',','')
            max_price = tds[2].string.replace(',','')
            min_price = tds[3].string.replace(',','')
            end_price = tds[4].string.replace(',','')
            volume = tds[5].string.replace(',','')
            self.register.setStockDate(self.stock.code, date, start_price, max_price, min_price, end_price, volume)
        except IndexError:
            pass
        yield self.register

    def setStock(self, stock):
        self.stock = stock
