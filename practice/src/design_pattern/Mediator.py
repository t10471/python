# -*- coding: utf-8 -*-
#オブジェクトの仲介をするクラス
#互いに依存している


class User(object) :
    def __init__(self, name) :
        self.name = name

    def getName(self) :
        return self.name

    def setChatroom(self, value) :
        self.chatroom = value

    def getChatroom(self) :
        return self.chatroom

    def sendMessage(self, to, message):
        self.chatroom.sendMessage(self.name, to, message)

    def receiveMessage(self, ffrom, message):
        print(u'%sさんから%sさんへ： %s' % (ffrom, self.getName(), message))



class Chatroom(object) :
    def __init__(self):
        self.users = {}
    def login(self,  user) :
        user.setChatroom(self)
        if user.getName() not in self.users :
            self.users[user.getName()] = user
            print(u'%sさんが入室しました' % user.getName())

    def sendMessage(self, ffrom, to, message) :
        if to in self.users :
            self.users[to].receiveMessage(ffrom, message)
        else :
            print(u'%sさんは入室していないようです' % to)



if __name__ == "__main__":
    chatroom = Chatroom()

    sasaki = User(u'佐々木')
    suzuki = User(u'鈴木')
    yoshida = User(u'吉田')
    kawamura = User(u'川村')
    tajima = User(u'田島')

    chatroom.login(sasaki)
    chatroom.login(suzuki)
    chatroom.login(yoshida)
    chatroom.login(kawamura)
    chatroom.login(tajima)

    sasaki.sendMessage(u'鈴木', '来週の予定は？')
    suzuki.sendMessage(u'川村', '秘密です')
    yoshida.sendMessage(u'萩原', '元気ですか？')
    tajima.sendMessage(u'佐々木', 'お邪魔してます')
    kawamura.sendMessage(u'吉田', '私事で恐縮ですが・・・')