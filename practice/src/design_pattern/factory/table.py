# -*- coding: utf-8 -*-

import factory
class TableFactory(factory.Factory):
    def createLink(self, caption, url):
        return TableLink(caption, url)
    def createTray(self, caption):
        return TableTray(caption)
    def createPage(self, title, author):
        return TablePage(title, author)

class TableLink(factory.Link):
    def __init__(self, caption, url):
        super(TableLink, self).__init__(caption, url)
    def makeHTML(self):
        return '<td><a href="%s">%s</a></td>\n' %(self.url, self.caption)

class TableTray(factory.Tray):
    def __init__(self, caption):
        super(TableTray, self).__init__(caption)
    def makeHTML(self):
        self.buffer = []
        self.buffer.append("<td>")
        self.buffer.append('<table width="100%" border="1"><tr>')
        self.buffer.append('<td bgcolor="#cccccc" align="center" colspan="%s"><b>%s</b></td>' %(len(self.tray), self.caption))
        self.buffer.append("</tr>\n")
        self.buffer.append("<tr>\n")
        for item in self.tray:
            self.buffer.append(item.makeHTML())
        self.buffer.append("</tr></table>")
        self.buffer.append("</td>")
        return "\n".join(self.buffer)

class TablePage(factory.Page):
    def __init__(self, title, author):
        super(TablePage, self).__init__(title, author)
    def makeHTML(self):
        self.buffer = []
        self.buffer.append("<html><head><title>%s</title></head>\n" %self.title)
        self.buffer.append("<body>\n")
        self.buffer.append("<h1>%s</h1>\n" %self.title)
        self.buffer.append('<table width="80%" boder="3">\n')
        for item in self.content:
            self.buffer.append("<tr>%s</tr>" %item.makeHTML())
        self.buffer.append("</table>\n")
        self.buffer.append("<hr><address>%s</address>" %self.author)
        self.buffer.append("</body></html>\n")
        return "\n".join(self.buffer)
