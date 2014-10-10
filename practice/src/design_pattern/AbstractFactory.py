# -*- coding: utf-8 -*-

#FactoryのFacotry
#Facotryでは単一のクラスの生成だが、
#AbstratFacoryでは複数の関連したクラスの生成を行う

class FileFactory(object):
    def createReader(self):
        pass
    def createWriter(self):
        pass

class CSVFactory(FileFactory):
    def createReader(self, file):
        return CSVReader(file)
    def createWriter(self):
        return CSVWriter(file)

class XMLactory(FileFactory):
    def createReader(self, file):
        return XMLReader(file)
    def createWriter(self):
        return XMLWriter(file)

class Reader(object):
    def __init__(self, file):
        self.file = file
    def read(self):
        pass
class XMLReader(Reader):
    def read(self):
        pass
class CSVReader(Reader):
    def read(self):
        pass

class Writer(object):
    def __init__(self, file):
        self.file = file
    def write(self):
        pass
class XMLWriter(Writer):
    def write(self):
        pass
class CSVWriter(Writer):
    def write(self):
        pass