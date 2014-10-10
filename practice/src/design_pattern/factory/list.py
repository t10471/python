# -*- coding: utf-8 -*-

import factory
class ListFactory(factory.Factory):
    def createLink(self, caption, url):
        return ListLink(caption, url)
    def createTray(self, caption):
        return ListTray(caption)
    def createPage(self, title, author):
        return ListPage(title, author)

class ListLink(factory.Link):
    def __init__(self, caption, url):
        super(ListLink, self).__init__(caption, url)
    def makeHTML(self):
        return ' <li><a href="%s">%s</a></li>\n' %(self.url, self.caption)

class ListTray(factory.Tray):
    def __init__(self, caption):
        super(ListTray, self).__init__(caption)
    def makeHTML(self):
        self.buffer = []
        self.buffer.append("<li>\n")
        self.buffer.append("%s\n" %self.caption)
        self.buffer.append("<ul>\n")
        for item in self.tray:
            self.buffer.append(item.makeHTML())
        self.buffer.append("</ul>\n")
        self.buffer.append("</li>\n")
        return "\n".join(self.buffer)

class ListPage(factory.Page):
    def __init__(self, title, author):
        super(ListPage, self).__init__(title, author)
    def makeHTML(self):
        self.buffer = []
        self.buffer.append("<html><head><title>%s</title></head>\n" %self.title)
        self.buffer.append("<body>\n")
        self.buffer.append("<h1>%s</h1>\n" %self.title)
        self.buffer.append("<ul>\n")
        for item in self.content:
            self.buffer.append(item.makeHTML())
        self.buffer.append("</ul>\n")
        self.buffer.append("<hr><address>%s</address>" %self.author)
        self.buffer.append("</body></html>\n")
        return "\n".join(self.buffer)

