import t10471.html.getter as hgetter
import mechanicalsoup
import datetime

class HtmlGetter(hgetter.HtmlGetter):

    def __init__(self, url):
        super(HtmlGetter, self).__init__(url)
        self.br = mechanicalsoup.Browser(soup_config={'features':'html.parser'})

    def get(self, stock, today, delta):
        start = (today - datetime.timedelta(days=delta)).strftime("%Y/%m/%d")
        sy, sm, sd = start.split('/')
        ey, em, ed = today.strftime("%Y/%m/%d").split('/')
        url = self.url % (stock.code, stock.market_code, sy, sm, sd, ey, em, ed)
        total = 0
        # 株式の取引日の方がdeltaより少ないので必ずIndexErrorになる
        try:
            page, trs = self.getRow(url)
            while (True):
                for tr in trs:
                    total += 1
                    yield tr
                    if total > delta:
                        return
                    url = page.soup.find_all('a', string='次へ')[0].get('href')
                page, trs = self.getRow(url)
        except IndexError:
            return

    def getRow(self, url):
        page = self.br.get(url)
        trs = page.soup.select('table.boardFin')[0].find_all('tr')
        trs.pop(0)
        return page, trs
