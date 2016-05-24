import CaboCha
import MeCab
import csv
import os

class Sentiment():

    def __init__(self):
        self.m = MeCab.Tagger()
        self.c = CaboCha.Parser()
        self.fPath = os.path.abspath(os.path.dirname(__file__)) + '/pn_ja.dic'
        self.table = type('Table', (dict,),
                          {'__missing__':lambda self,key:{'type':None, 'num':0.0}})()
        self.loadTable()

    def loadTable(self):
        with open(self.fPath, newline='', encoding='sjis') as csvfile:
            records = csv.reader(csvfile, delimiter=':', quotechar='|')
            for record in records:
                value = {'type':record[2], 'num':record[3]}
                self.table.update({record[0] : value})
                self.table.update({record[1] : value})

    def run(self, text):
        # m = self.m.parseToNode(text)
        # while m:
        #     print(m.surface, m.feature)
        #     m = m.next
        parsed = self.c.parse(text)
        dics = self.extract(parsed)
        dics = self.addScore(dics)
        dics = self.reverse(dics)

    def extract(self, parsed):
        dics = []
        for i in range(parsed.chunk_size()):
            chunk = parsed.chunk(i)
            features = []
            bases = []
            normalizeds = []
            for ix in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                normalizeds.append(parsed.token(ix).normalized_surface)
                features.append(parsed.token(ix).feature.split(','))
                bases.append(features[-1][6])
            dics.append({'bases':bases, 'normalizeds':normalizeds, 'features':features})
        return dics

    def addScore(self, dics):
        for i,dic in enumerate(dics):
            dics[i]['score'] = [self.table[base] for base in dic['bases']]
        return dics

    def reverse(self, dics):
        print(dics)
        # exit()
        pass

    def print(self, parsed):
        print(parsed.toString(CaboCha.FORMAT_TREE))
        print(parsed.toString(CaboCha.FORMAT_LATTICE))
        print(parsed.toString(CaboCha.FORMAT_TREE_LATTICE))
        print(parsed.toString(CaboCha.FORMAT_XML))
