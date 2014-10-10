# -*- coding: utf-8 -*-
import unicodedata

#chain of responseibilityのchainしない番
#それぞれの処理を小さくし、
#それらを自由に付け替えられるようにする
#handlerに各処理を登録し、実行する

class PlainText(object):

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

class TextDecorator(object):
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text.getText()

    def setText(self, text):
        self.text.setText(text)



class UpperCaseText(TextDecorator):
    def __init__(self, text):
        super(UpperCaseText, self).__init__(text)

    def getText(self):
        text = super(UpperCaseText, self).getText()
        return text.title()

class DoubleByteText(TextDecorator):
    def __init__(self, text):
        super(DoubleByteText, self).__init__(text)

    def getText(self):
        text = super(DoubleByteText, self).getText()
        return unicodedata.normalize('NFKC', text)


if __name__ == '__main__':

        txt = PlainText()
        txt.setText(u'ｱ 12 １２ af de')
        print DoubleByteText(UpperCaseText(txt)).getText()
