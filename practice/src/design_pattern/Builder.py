# -*- coding: utf-8 -*-
from msilib import Directory

#オブジェクトの「生成手順」と「生成手段」を分ける
#DrirectorとBuilderに分かれる
#基本Bridgeと同様に委譲を行うが、
#違いはDirectorの引数がBuilderとBuilderが使う要素
#Drectorがそのあたりのコントロールを行う
#Facadeに近い感じで、Directorのメソッドはまとめてある？

class News(object):
    def __init__(self, title, url, data):
        self.title = title
        self.url   = url
        self.data  = data
    def getTitle(self):
        return self.title
    def getUrl(self):
        return self.url
    def getData(self):
        return self.data

class NewsDirector(object):
    def __init__(self, builder, url):
        self.builder = builder
        self.url = url

    def getNews(self):
        news_list = self.builder.parse(self.url);
        return news_list;

class RssNewsBuilder(object):
    def parse(self,url):
        #Newsの配列を返す
        pass

builder = RssNewsBuilder()
url = 'http://www.php.net/news.rss';

director = NewsDirector(builder, url);
for news in director.getNews():
    print '%s %s %s' % news.getData, news.getUrl(), news.getTitle()
