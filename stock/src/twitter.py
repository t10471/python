import path
path.dummy()
from t10471.twitter.streaming import MyStreaming
from t10471.analysis.word.sentiment import Sentiment
class TwitterMain(object):

    def __init__(self):
        pass

    def run(self):
        sen = Sentiment()
        # MyStreaming().run()
        words = ['アクションシーンがよかった',
                 'よくまとまっているとはお世辞にも言えない',
                 '具合が悪くてあまり食べられなかった',
                 'お金がない',
                 '夢や希望がない',
                 'ケガが無くて良かった',
                 '忙しくないことはない',
                 '仕事がないわけではない',
                 '海に行かない？',
                 '宝くじが当たらないかな？',
                 '君の言うことは分からないこともない',
                 '君がそれをできないわけがない',
                 '色がきれいじゃない',
                 '一度決めたら変えられない',
                 '財布が見つからないんです。ここになかったですか？',
                 '警察は安全管理に問題がなかったかどうか調べています',
                 '空いている席はないですか？',
                 '彼が死んだことを知らなかった',
                 '質問に答えられなかった',
                 '満腹で食べられなかった',
                 '仕事がなかった間、勉強していました']
        for word in words:
            sen.run(word)
        pass

if __name__ == '__main__':
    TwitterMain().run()
