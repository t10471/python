
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
import t10471.twitter.config as config

class MyAouth():

    def auth():
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
        return auth


class MyListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.cnt = 0
        self.limit = 100

    def on_status(self, status):
        if self.strategry is not None:
            self.strategy.run(status.text)
        # print(status.text)
        if self.isLimit():
            return False

    def isLimit(self):
        self.cnt += 1
        if self.cnt > self.limit :
            return True
        return False

    def on_error(self, status_code):
        print(status_code)
        return False

    def setStrategy(self, strategy):
        self.strategy = strategy

class MyStreaming():

    def __init__(self):
        self.strategy = None

    def run(self):
        listener = MyListener()
        if self.strategy is not None:
            listener.setStrategy(self.strategy)
        Stream(MyAouth.auth(),listener).sample(languages=['ja'])

    def setStrategy(self, strategy):
        self.strategy = strategy
