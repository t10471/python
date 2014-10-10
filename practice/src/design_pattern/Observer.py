# -*- coding: utf-8 -*-

#処理のあとに通知して更新
import pprint

class Cart(object):
    def __init__(self):
        self.items = {}
        self.listeners = {}

    def addItem(self, item_cd):
        if item_cd in self.items:
            self.items[item_cd] += 1
        else:
            self.items[item_cd] = 1
        self.notify()

    def removeItem(self, item_cd):
        if item_cd in self.items:
            self.items[item_cd] -= 1
        else:
            self.items[item_cd] = 0
        if self.items[item_cd] <= 0:
            del self.items[item_cd]
        self.notify()

    def getItems(self):
        return self.items

    def hasItem(self, item_cd):
        return True if item_cd in self.items else False

    #Observerを登録するメソッド
    def addListener(self, listener):
        self.listeners[listener.__class__.__name__] = listener

    #Observerを削除するメソッド
    def removeListener(self,listener):
        del self.listeners[listener.__class__.__name__]

    #Observerへ通知するメソッド
    def notify(self):
        for listener in self.listeners.values():
            listener.update(self)

class PresentListener(object):


    def __init__(self):
        self.PRESENT_TARGET_ITEM = u'30:クッキーセット'
        self.PRESENT_ITEM = u'99:プレゼント'

    def update(self, cart):
        if cart.hasItem(self.PRESENT_TARGET_ITEM) and not cart.hasItem(self.PRESENT_ITEM):
            cart.addItem(self.PRESENT_ITEM)

        if not cart.hasItem(self.PRESENT_TARGET_ITEM) and cart.hasItem(self.PRESENT_ITEM):
            cart.removeItem(self.PRESENT_ITEM)

class LoggingListener(object):

    def __init__(self):
        pass

    def update(self, cart):
        pprint.pprint(cart.getItems())

def ctr(mode, cart, item):
    if mode == 'add':
        print '追加しました'
        cart.addItem(item)
    elif mode == 'remove':
        print '削除しました'
        cart.removeItem(item)
    elif mode == 'clear':
        print 'クリアしました'
        cart = createCart()

    print '商品一覧'
    for item_name, quantity in cart.getItems().items():
        print item_name + u' ' + str(quantity) + u'個'

def createCart():
    cart = Cart()
    cart.addListener(PresentListener())
    cart.addListener(LoggingListener())

    return cart

if __name__ == "__main__":

    cart = createCart()

    ctr('add', cart, u'10:Tシャツ')
    ctr('add', cart, u'20:ぬいぐるみ')
    ctr('add', cart, u'20:ぬいぐるみ')
    ctr('add', cart, u'30:クッキーセット')
    ctr('remove', cart, u'20:ぬいぐるみ')
    ctr('clear', cart, u'30:クッキーセット')

