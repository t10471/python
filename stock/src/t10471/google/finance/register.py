import csv
import t10471.google.finance.formatter as formatter
from datetime import datetime

class Register():

    def __init__(self):
        pass

    def write(self, path, data):
        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=formatter.COLS)
            writer.writeheader()
            DATE = formatter.DATE
            for row in data:
                row[DATE] = datetime.strftime(row[DATE], '%Y-%m-%d %H:%M:%S')
                writer.writerow(row)
