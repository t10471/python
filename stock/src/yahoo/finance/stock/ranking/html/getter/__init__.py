# -*- coding: utf-8 -*-

import html.getter
import mechanize

class HtmlGetter(html.getter.HtmlGetter):
    def __init__(self, url):
        super(HtmlGetter, self).__init__(url)

    def get(self):
        """main(銘柄コード)"""
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(self.url)
        br.follow_link(text_regex = "株式ランキング")
        word = unicode('出来高',"utf-8").encode("euc-jp")
        data = br.follow_link(text_regex = word)
        yield self._translate(data)

        word = unicode('次の50件',"utf-8").encode("euc-jp")
        for cnt in range(1,10): #@UnusedVariable
            data = br.follow_link(text_regex = word)
            #htmlが返る
            yield self._translate(data)

    def _translate(self, data):
        return unicode(data.read(),"euc-jp").encode("utf-8")
