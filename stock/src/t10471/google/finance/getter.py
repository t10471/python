import urllib.request

class Getter():

    def __init__(self, url):
        self.url = url
        self.interval_day = 86400
        self.interval_min = 300

    def get_day(self, period, term, market, symbol, ts):
        period = period + term
        return self.get(period, self.interval_day, market, symbol, ts)

    def get_min(self, period, term, market, symbol, ts):
        period = period + term
        return self.get(period, self.interval_min, market, symbol, ts)

    def get(self, period, interval, market, symbol, ts):
        url = self.url.format(period, interval, market, symbol, ts)
        print(url)
        with urllib.request.urlopen(url) as u:
            data = u.read()
        return data.decode('utf8').split('\n')
