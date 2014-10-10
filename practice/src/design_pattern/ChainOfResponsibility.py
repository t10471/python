# -*- coding: utf-8 -*-
import re

#ポインタでオブジェクト間をつなぐ
#それぞれの処理を小さくし、
#それらを自由に付け替えられるようにする
#handlerに各処理を登録し、実行する

class ValidationHandler(object):
    def __init__(self):
        self.next_handler = None

    def setHandler(self, handler):
        self.next_handler = handler
        return self

    def getNextHandler(self):
        return self.next_handler

    def validate(self, input):
        result = self.execValidation(input)
        if (result is not True):
            return self.getErrorMessage()
        elif (self.getNextHandler() is not None):
            return self.getNextHandler().validate(input)
        else:
            return True

    def execValidation(self, input):
        pass

    def getErrorMessage(self):
        pass

class AlphabetValidationHandler(ValidationHandler):
    def execValidation(self, input):
        return True if re.match('^[a-z]*', input, re.IGNORECASE) else False


    def getErrorMessage(self) :
        return u'半角英字で入力してください'



class NumberValidationHandler(ValidationHandler):

    def execValidation(self, input) :
        return True if re.match('^[0-9]*', input, re.IGNORECASE) else False


    def getErrorMessage(self) :
        return u'半角数字で入力してください'



class NotNullValidationHandler(ValidationHandler ):

    def execValidation(self, input) :
        return len(input) != 0


    def getErrorMessage(self) :
        return u'入力されていません'


class MaxLengthValidationHandler(ValidationHandler ):

    #ここから
    def __init__(self, max_length = 10) :
        super(ValidationHandler, self).__init__()

        if re.match(r'^[0-9]{0,2}$', str(max_length)) is None:
            raise  Exception, 'max length is invalid (0-99) !'

        self.max_length = max_length


    def execValidation(self, input) :
        return len(input) <= self.max_length


    def getErrorMessage(self) :
        return self.max_length + u'バイト以内で入力してください'


if __name__ == '__main__':

        validate_type = 'num'
        input = 'aaaa'

        not_null_handler = NotNullValidationHandler()
        length_handler = MaxLengthValidationHandler(8)

        option_handler = None
        if validate_type == 'num':
            option_handler = NumberValidationHandler()
        else:
            option_handler = AlphabetValidationHandler()



        if option_handler != None:
            length_handler.setHandler(option_handler)

        handler = not_null_handler.setHandler(length_handler)

        result = handler.validate(input)
        if  isinstance(result, bool) and result == False:
            print  u'検証できませんでした'
        elif not isinstance(result, bool) and result != None :
            print result
        else:
            print 'ok'
