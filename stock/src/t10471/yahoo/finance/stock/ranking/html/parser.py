# -*- coding: utf-8 -*-

import t10471.html.parser as hparser
import mechanicalsoup
from urllib.parse import urlparse

class HtmlParser(hparser.HtmlParser):

    def __init__(self, register):
        super(HtmlParser, self).__init__()
        self.register = register
        self.br = mechanicalsoup.Browser(soup_config={'features':'html.parser'})

    def parse(self, soup):
        self.list =  soup.find_all('tr', class_='rankingTabledata')
        for row in self.list:
            tds = row.find_all('td')
            market_name = tds[2].string
            url = tds[1].find('a').get('href')
            st, market_code = urlparse(url).query.split('.')
            rm, stock_code = st.split('=')
            self.setMarket(market_code, market_name)
            page = self.br.get(url)
            try:
                business_name = page.soup.select('dl.stocksInfo')[0].select('dd.category')[0].select('a')[0].string
            except IndexError:
                business_name = page.soup.select('dl.stocksInfo')[0].select('dd.category')[0].string
            self.setBusiness(business_name)
            business_code = self.register.getBusinessCode()
            stock_name = tds[3].string
            self.setStock(stock_code, stock_name, market_code, business_code)
            yield self.register

    def setMarket(self, code, name):
        self.register.setMarket(code, name)

    def setBusiness(self, name):
        self.register.setBusiness('', name)

    def setStock(self, code, market_code, name, business_code):
        self.register.setStock(code, name, market_code, business_code)
