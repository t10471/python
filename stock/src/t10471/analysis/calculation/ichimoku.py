import Calculation

class Ichimoku(Calculation):

    def __init_(self):
        pass

    # 転換線      (9日間の高値 + 9日間の安値) / 2
    # 基準線      (26日間の高値 + 26日間の安値) / 2
    # 先行スパン1 (基準線 + 転換線) / 2 を26日先にスライド
    # 先行スパン2 (52日間の高値 + 52日間の安値) / 2 を26日先にスライド
    # 遅行スパン  終値を26日前にスライド
    def calculate(self, data):
        length = len(data)
        base_span = 26
        shift_span = 9
        preceding_span = 52
        bases = shifts = precedings1 = precedings2 = delays = []
        dummy, prices = self.dataSplit(data)
        for x in range(0, length):
            if x < shift_span:
                bases.append((data[x][0],None))
                shifts.append((data[x][0],None))
                precedings1.append((data[x][0],None))
                precedings2.append((data[x][0],None))
                delays.append((data[x][0], None))
                continue
            if x > shift_span:
                shifts.append((data[x][0], self.calMid(x, prices, shift_span)))
            else:
                shifts.append((data[x][0],None))
            if x > base_span:
                bases.append((data[x][0], self.calMid(x, prices, base_span)))
                precedings1.append((data[x + base_span][0], int((bases[x][1] + shifts[x][1]) / 2)))
                delays.append((data[x - base_span][0], data[x][1]))
            else:
                bases.append((data[x][0],None))
                precedings1.append((data[x + base_span][0], None))
                delays.append((data[x + base_span][0], None))
            if x > preceding_span:
                precedings2.append((data[x + base_span][0], self.calMid(x, prices, preceding_span)))
            else:
                precedings2.append((data[x + base_span][0], None))
        return {'bases' : bases,
                'shifts' : shifts,
                'precedings1' : precedings1,
                'precedings2' : precedings2,
                'delays' : delays}

    def dataSplit(self, data):
        date = []
        price = []
        for d in data:
            date.append(d[0])
            price.append(d[1])
        return date,price

    def calMid(self, x, data, span):
        max_d = max(data[(x - span):x])
        min_d = min(data[(x - span):x])
        return int((max_d + min_d) / 2)
