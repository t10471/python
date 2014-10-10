# -*- coding: utf-8 -*-

import sys

class LoginCheck:
    """
    This class checks whether a user
    has logged in properly via
    the global "check_function". If so,
    the requested routine is called.
    Otherwise, an alternative page is
    displayed via the global "alt_function"
    """
    def __init__(self, f):
        #実行時のメソッド名の取得
        print sys._getframe().f_code.co_name

        self._f = f

    def __call__(self, *args):
        print sys._getframe().f_code.co_name

        Status = check_function()
        if Status==1:
            return self._f(*args)
        else:
            return alt_function()

def check_function():
    return test

def alt_function():
    print 'Sorry - this is the forced behaviour'

print 1
@LoginCheck
def display_members_page():
    print 'This is the members page'

print 2
test = 0
#デコレータに引数がないから__call__はこのタイミングで呼ばれる
display_members_page()
# Displays "Sorry - this is the forced behaviour"

print 3
test=1
display_members_page()
# Displays "This is the members page"