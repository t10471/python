
class RSI():

    def __init_(self):
        pass

    # 相対力指数
    # (値上がり合計 / 値上がり合計 + 値下がり合計) * 100
    def calculate(self, data, span):
        buff = []
        for x in range(len(data) - span):
            if x == 0:
                continue
            delta = up = down = 0.0
            for j in range(span):
                    delta  = data[x + j][1] - data[x + j - 1][1]
                    if delta > 0 :
                        up += delta
                    else:
                        down += abs(delta)
            sri = (up / up + down) * 100
            buff.append((data[x +  span][0], sri))
        return buff
