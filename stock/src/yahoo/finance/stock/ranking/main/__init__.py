# -*- coding: utf-8 -*-

import yahoo.finance.stock.ranking.html.getter
import yahoo.finance.stock.ranking.html.parser
import model.register

class Main(object):
    def __init__(self):
        self.getter = yahoo.finance.stock.ranking.html.getter.HtmlGetter('http://stocks.finance.yahoo.co.jp/')
        self.parser = yahoo.finance.stock.ranking.html.parser.HtmlParser(model.register.Register())

    def run(self):
        for html in self.getter.get():
            for register in self.parser.parse(html, self.register):
                register.RegisterStockBaseInfo()
