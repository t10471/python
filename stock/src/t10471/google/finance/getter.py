import urllib.request
from urllib.error import HTTPError

class Getter():

    def __init__(self, url):
        self.url = url
        self.interval_day = 86400
        self.interval_min = 300

    def get_day(self, period, term, market, symbol):
        period = period + term
        return self.get(period, self.interval_day, market, symbol)

    def get_min(self, period, term, market, symbol):
        period = period + term
        return self.get(period, self.interval_min, market, symbol)

    def get(self, period, interval, market, symbol):
        url = self.url.format(period, interval, market, symbol)
        try:
            u = urllib.request.urlopen(url)
            data = u.read()
        except HTTPError as e:
            print("ERROR {0}, {1}, {2} ".format(e.code, market, symbol))
            raise e
        return data.decode('utf8').split('\n')
