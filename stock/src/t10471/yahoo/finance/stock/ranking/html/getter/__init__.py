import t10471.html.getter as hgetter
import mechanicalsoup

class HtmlGetter(hgetter.HtmlGetter):

    def __init__(self, url):
        super(HtmlGetter, self).__init__(url)

    def get(self):
        br = mechanicalsoup.Browser(soup_config={'features':'html.parser'})
        page = br.get(self.url)
        url = page.soup.find('a', string='株式ランキング').get('href')
        page = br.get(url)
        url = page.soup.find('a', string='出来高').get('href')
        page = br.get(url)
        yield page.soup

        for cnt in range(1,10):
            url = page.soup.find('a', string='次へ').get('href')
            page = br.get(url)
            yield page.soup
