# -*- coding: utf-8 -*-

#状態をクラスとしてクラスの中に持ち
#状態ごとにクラスとする


class User(object):

    def __init__(self, name):
        self.name = name
        self.count = 0
        #初期値
        self.state = UnauthorizedState.getInstance()
        self.resetCount()

    # 状態を切り替える
    def switchState(self):
        print "状態遷移:" + self.state.__class__.__name__ + "→"
        self.state = self.state.nextState()
        print self.state.__class__.__name__
        self.resetCount()

    def isAuthenticated(self):
        return self.state.isAuthenticated()


    def getMenu(self):
        return self.state.getMenu()


    def getUserName(self):
        return self.name


    def getCount(self):
        return self.count


    def incrementCount(self):
        self.count += 1

    def resetCount(self):
        self.count = 0

class AuthorizedState(object):

    singleton = None
    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls.singleton is None:
            cls.singleton = AuthorizedState()

        return cls.singleton


    def isAuthenticated(self):
        return True

    def nextState(self):
        # 次の状態（未認証）を返す
        return UnauthorizedState.getInstance()


    def getMenu(self):
        menu = 'カウントアップ | ' \
              +    'リセット | '\
              +    'ログアウト'
        return menu



class UnauthorizedState(object):

    singleton = None
    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls.singleton is None:
            cls.singleton = UnauthorizedState()

        return cls.singleton


    def isAuthenticated(self):
        return False


    def nextState(self):
        # 次の状態（認証）を返す
        return AuthorizedState.getInstance()


    def getMenu(self):
        menu = 'ログイン'
        return menu

if __name__ == "__main__":

    context = User('ほげ')

    print '状態を遷移します'
    context.switchState()
    print 'カウントアップします'
    context.incrementCount()

    print 'ようこそ、' + context.getUserName() + 'さん'
    print '現在、ログインして' +  'います' if  context.isAuthenticated() else 'いません'
    print '現在のカウント：' + str(context.getCount())
    print context.getMenu()

    print 'カウントをリセットします'
    context.resetCount()

    print '現在のカウント：' +str(context.getCount())

    print '状態を遷移します'
    context.switchState()

    print 'ようこそ、' + context.getUserName() + 'さん'
    print '現在、ログインして' +  ('います' if  context.isAuthenticated() else 'いません')
    print '現在のカウント：' + str(context.getCount())
    print context.getMenu()
