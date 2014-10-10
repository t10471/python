# -*- coding: utf-8 -*-

#Adapterパターンみたいに委譲をつかう
#代理応答



class Item(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

class DbItemDao(object):
    def findById(self, item_id):
        item = None
        with file('item_data.txt') as lines:
            try:
                next(lines)
            except Exception as e:
                return item
            for line in lines:
                id = line[0:10].strip()
                name = line[10:].strip()
                if item_id == int(id):
                    item = Item(id, name)
                    break
        return item

class MockItemDao(object):
    def findById(self, item_id):
        item = Item(item_id, 'ダミー商品')
        return item

class ItemDaoProxy(object):
    def __init__(self, dao):
        self.dao = dao
        self.cache = {}

    def findById(self, item_id):
        if item_id in self.cache:
            print 'Proxyで保持しているキャッシュからデータを返します'
            return self.cache[item_id]

        self.cache[item_id] = self.dao.findById(item_id)
        return self.cache[item_id]

if __name__ == "__main__":

    dao = MockItemDao()
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'
    dao = ItemDaoProxy(dao)
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'
    dao = DbItemDao()
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'
    dao = ItemDaoProxy(dao)
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'
    for item_id in range(1,4):
        item = dao.findById(item_id)
        print 'ID=' + str(item_id) + 'の商品は「' + item.getName() + '」です'

