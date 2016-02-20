import Calculation

class EMAverage(Calculation):

    def __init_(self):
        pass

    # span日数の指数平滑移動平均線
    # n日間の指数平滑移動平均
    # 1日目＝(当日も含め)n日の終値の平均
    # 2日目以降＝前日の指数平滑移動平均 + α * (当日終値-前日の指数平滑移動平均)
    # ※ α(平滑定数)  = 2 / (n + 1)
    def calculate(self, data, span):
        buff = []
        for x in range(len(data) - span):
            y = 0.0
            if(x == 0):
                # 最初は単純移動平均
                for j in range(span):
                    y += data[x + j][1]
                y /= span
            else :
                y = buff[x - 1][1]
            ema = y + (2 / span + 1) * (data[x + span][1] - y)
            buff.append((data[x + span][0], ema))
        return buff
