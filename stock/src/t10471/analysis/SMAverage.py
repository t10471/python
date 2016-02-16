import Calculation

class SMAverage(Calculation):

    def __init_(self):
        pass

    # span日数の単純移動平均
    def calculate(self, data, span):
        buff = []
        for x in range(len(data) - span):
            y = 0.0
            for j in range(span):
                y += data[x + j][1]
            y /= span
            buff.append((data[x +  span][0], y))
        return buff
