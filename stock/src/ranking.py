import path
path.dummy()
import t10471.yahoo.finance.stock.ranking.html.getter as getter
import t10471.yahoo.finance.stock.ranking.html.parser as parser
import t10471.model.register as register

class Ranking(object):

    def __init__(self):
        self.getter = getter.HtmlGetter('http://stocks.finance.yahoo.co.jp/')
        self.register = register.Register()
        self.parser = parser.HtmlParser(self.register)

    def run(self):
        for soup in self.getter.get():
            for rg in self.parser.parse(soup):
                rg.RegisterStock()
        self.register.commit()

if __name__ == '__main__':
    Ranking().run()
