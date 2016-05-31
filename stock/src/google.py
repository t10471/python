# -*- coding: utf-8 -*-

import path
path.dummy()
import t10471.google.finance.getter as getter
import t10471.google.finance.parser as parser
import t10471.google.finance.register as register
import t10471.google.finance.formatter as formatter
from datetime import datetime, date
import os
import os.path as op
import csv
import codecs

TERM = 'term'
DIR = 'dir'
METHOD = 'method'
MIN = {TERM: 'd', DIR: 'min', METHOD: 'get_min'}
DAY = {TERM: 'd', DIR: 'day', METHOD: 'get_day'}

class Google(object):

    def __init__(self):
        url = 'http://www.google.com/finance/getprices?p={0}&f=d,h,o,l,c,v&i={1}&x={2}&q={3}&ts={4}'
        self.getter = getter.Getter(url)
        self.parser = parser.Parser()
        self.register = register.Register()
        self.start = date(2000, 1, 1)

    def run(self, term_type):
        span = (date.today() - self.start).days
        ts = datetime.now().strftime('%s')
        in_data = self._parse_tsv(op.join(op.join(op.abspath(os.getcwd()), 'japan-all-stock-prices.tsv')))
        for code, symbol in in_data:
            print("code {0}, symbol {1}".format(code, symbol))
            method = getattr(self.getter, term_type[METHOD])
            data = self.parser.parse(method(str(span), term_type[TERM], code, symbol, ts))
            if len(data) != 0:
                print(data[0][formatter.DATE])
            stock_dir = self._mkdir(op.join(op.abspath(os.getcwd()), 'output', 'stocks', term_type[DIR]))
            self.register.write(op.join(stock_dir, symbol + '.csv'), data)

    def _mkdir(self, d):
        try:
            os.mkdir(d)
        except FileExistsError:
            pass
        return d

    def _parse_tsv(self, fn):
        with codecs.open(fn, 'r', 'utf-16') as fp:
            return [('TYO', row['SC']) for row in csv.DictReader(fp, delimiter='\t')]

if __name__ == '__main__':
    Google().run(DAY)
