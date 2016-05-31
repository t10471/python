from datetime import datetime
from datetime import timedelta
import csv
import t10471.google.finance.formatter as formatter

COLUMNS = 'COLUMNS'
INTERVAL = 'INTERVAL'
TIMEZONE_OFFSET = 'TIMEZONE_OFFSET'
DATE = formatter.DATE

class Parser():

    def __init__(self):
        pass

    def parse(self, data):
        head, rows = self._split(data[1:])
        if len(rows) == 0:
            return rows
        try:
            self.cols = head[COLUMNS].split(',')
            self.interval = int(head[INTERVAL])
            self.offset = int(head[TIMEZONE_OFFSET]) * 60
        except KeyError:
            return []
        self.base_time = None
        return self._parse(rows)

    def _parse(self, rows):
        results = []
        for row in csv.reader(rows, delimiter=','):
            if len(row) == 0:
                continue
            results.append(self._convert_date(dict(zip(self.cols, row))))
        return results

    def _convert_date(self, array):
        if array[DATE].startswith('a'):
            t = float(array[DATE].replace('a', '')) + self.offset
            self.base_time = datetime.fromtimestamp(t)
            array[DATE] = self.base_time
        else:
            s = int(array[DATE]) * self.interval
            array[DATE] = self.base_time  + timedelta(seconds=s)
        return array

    def _split(self, data):
        head = None
        for i, r in enumerate(data):
            if r.find('=') == -1:
                head = data[0:i]
                rows = data[i:]
                break
        if head is None:
            head = data
            rows = []
        return self._convert_head(head), rows

    def _convert_head(self, data):
        results = []
        for r in data:
            results.append(tuple(r.split('=')))
        return dict(results)
