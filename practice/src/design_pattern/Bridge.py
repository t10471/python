# -*- coding: utf-8 -*-

#Adaptarパターンとほぼ同一
#Adaptarパターンが後付けなのに対して設計時に分けることで実現される
#機能(Listing)と実装(DataSource)を分けて作れる


class DataSource(object):
    def open(self):
        pass
    def read(self):
        pass
    def close(self):
        pass

class FileSource(DataSource):
    def __init__(self, filename):
        pass
    def open(self):
        pass
    def read(self):
        pass
    def close(self):
        pass

#実装側に委譲する
class Listing(object):
    def __init__(self, data_source):
        self.data_source = data_source;

    def open(self):
        return self.data_source.open()
    def read(self):
        return self.data_source.read()
    def close(self):
        return self.data_source.close()

class ExtendListing(Listing):
    def readWithEncode(self):
        return self.read().encode('utf-8')

fs = FileSource('a.txt')
el = ExtendListing(fs)
el.open()
el.read()
el.readWithEncode()
el.close()
