import path
path.dummy()
import t10471.yahoo.finance.stock.ranking.html.getter as ranking_getter
import t10471.yahoo.finance.stock.ranking.html.parser as ranking_parser
import t10471.model.register as register

class Main(object):

    def __init__(self):
        self.getter = ranking_getter.HtmlGetter('http://stocks.finance.yahoo.co.jp/')
        self.register = register.Register()
        self.parser = ranking_parser.HtmlParser(self.register)

    def run(self):
        for soup in self.getter.get():
            for rg in self.parser.parse(soup):
                rg.RegisterStock()
        self.register.commit()

if __name__ == '__main__':
    Main().run()
