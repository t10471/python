# -*- coding: utf-8 -*-

class Item(object):
    def __init__(self, caption):
        self.caption = caption
    def makeHTML(self):
        pass

class Link(Item):
    def __init__(self, caption, url):
        super(Link, self).__init__(caption)
        self.url = url

class Tray(Item):
    def __init__(self, caption):
        super(Tray, self).__init__(caption)
        self.tray = []
    def add(self, item):
        self.tray.append(item)

class Page(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.content = []
    def add(self, item):
        self.content.append(item)
    def output(self):
        self.filename = "%s.html" %self.title
        writer = open(self.filename, "w")
        writer.write(self.makeHTML())
        writer.close()
        print "%sを作成しました。" %self.filename
    def makeHTML(self):
        pass

class Test(object):
    def __init__(self):
        pass

#動的にロードする方法
class Factory(object):
    @classmethod
    def getFactory(cls, module):
        m = module.split( '.' )
        if len(m) == 1:
            return  globals()[module]()
        elif len(m) > 1:
            #__import__はパッケージのTOPしか読み込まないので、
            #サブ階層のはgetatterで取得する
            klass = m[-1]
            components = m[1:-1]
            mod = __import__(m[0])
            for c in components:
                mod = getattr( mod, c )
            return getattr( mod, klass )()

    def createLink(self, caption, url):
        pass
    def createTray(self, caption):
        pass
    def createPage(self, title, author):
        pass
