# -*- coding: utf-8 -*-

import html.parser
import re
from model.connection import get_session
from model.db import Stock, Market, Business
from beautiflSoupEx import get_yahoo_finance

class HtmlParser(html.parser.HtmlParser):
    def __init__(self, register = None):
        super(HtmlParser, self).__init__()
        self.register = register

    def parse(self, html):
        self.list =  get_yahoo_finance(html).findAll('td', bgcolor="#ffffff")
        method_list = {1:'_getCode', 2:'_getMarket',3: '_getName', 4:'_getBusiness'}
        while len(self.list) != 0:
            #if not re.search('<nobr>',link) :
            for i in range(1,13): #@UnusedVariable
                link = str(self.list.pop())
                if i in method_list:
                    method_list[i](link)
            yield self.register

    def _getCode(self, link):
        code = re.search('code=(.*?)">',link)
        if code:
            code = str(code.group(1))
            code = code.split('.')
            self.register.s_code = code[0]
            self.register.m_code = code[1]
    def _getMarket(self, link):
        mark = re.search('<small>(.*?)</small>',link)
        if mark:
            self.register.mark = str(mark.group(1))

    def _getName(self, link):
        name = re.search('">(.*?)<',link)
        if name:
            self.register.name = str(name.group(1))

    def _getBusiness(self, link):
        job = re.search('<small>(.*?)</small>',link)
        if job:
            self.register.job = str(job.group(1))
