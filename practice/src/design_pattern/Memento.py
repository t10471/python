# -*- coding: utf-8 -*-

#データの一時保存をする
#DataSnapshotが保存するデータ
#DataCaretakerがsnapshotを操作するクラス
#Dataがデータを操作するクラス
#Dataにしか操作権限をもたせない
#DataCaretakerは単なる出し入れ

from collections import defaultdict

class Singleton(type):
    def __new__(cls, name, bases, dict_):
        dict_['instance'] = None
        return type.__new__(cls, name, bases, dict_)

    def __call__(cls, *args): #@NoSelf
        if cls.instance == None:
            cls.instance = type.__call__(cls, *args)
            cls.__init__(cls.instance, *args)
        return cls.instance

class Session(defaultdict):
    __metaclass__=Singleton
    def __init__(self):
        super(Session, self).__init__(str)

class DataSnapshot(object):
    def __init__(self, comment):
        self.comment = comment

    def getComment(self):
        return self.comment

class Data(DataSnapshot):
    def __init__(self):
        self.comment = []

    def takeSnapshot(self):
        return DataSnapshot(self.comment)

    def restoreSnapshot(self, snapshot):
        self.comment = snapshot.getComment()

    def addComment(self, comment):
        self.comment.append(comment)

    def getComment(self):
        return self.comment


class DataCaretaker(object):

    def __init__(self):
        pass

    def setSnapshot(self, snapshot):
        self.snapshot = snapshot
        Session()['snapshot'] = self.snapshot

    def getSnapshot(self):
        return Session()['snapshot'] if Session()['snapshot'] != ''  else None

def add(mode, comment):
    print mode
    caretaker = DataCaretaker()
    data = Session()['data'] if  Session()['data'] != '' else Data()

    if mode == 'add':
        data.addComment(comment)
    elif mode == 'save':
        caretaker.setSnapshot(data.takeSnapshot())
        print 'データを保存しました。'
    elif mode == 'restore':
        data.restoreSnapshot(caretaker.getSnapshot())
        print 'データを復元しました。'
    elif mode == 'clear':
        data = Data()
    Session()['data'] = data
    show(data)
    return data

def show(data):
    print '今までのコメント'
    if data is not None:
        for comment in data.getComment():
            print comment

if __name__ == "__main__":

    mode = 'add'
    comment = 'aaaa'
    data = add(mode, comment)
    mode = 'add'
    comment = 'bbbb'
    data = add(mode, comment)
    mode = 'save'
    comment = 'cccc'
    data = add(mode, comment)
    mode = 'clear'
    comment = 'dddd'
    data = add(mode, comment)
    mode = 'restore'
    comment = 'eeee'
    data = add(mode, comment)
    mode = 'add'
    comment = 'ffff'
    data = add(mode, comment)


