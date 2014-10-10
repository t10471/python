# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParseError
import re, string

def get_yahoo_finance( html ,) :
    try:
        return BeautifulSoup(html)
    except HTMLParseError, e :
        return _handle_error(e, html)
    except Exception, e:
        # 想定外の例外の場合は再送出
        raise e

def _handle_error(e, html):
    e_malformed = "malformed start tag"
    e_junk = "junk characters in start tag: "
    if e.msg.find(e_malformed) != -1 :
        html = re.sub("<div.*;>", r'<div>', html)
        return get_yahoo_finance( html )
    elif e.msg.find( e_junk ) != -1 :
        # エラーメッセージに"junk characters in start tag: "が含まれる場合
        u"""
        エラーメッセージから"junk characters in start tag: "を取りのぞくと、
        エラーを引き起こしている文字列部分のみが取り出せます。
        BeautifulSoupの場合、受け取った文字列を内部でUnicode型に変換するため、
        取り出した文字列は u'xxxx' のような形になるので、一旦evalで評価して
        Unicode型のオブジェクトを生成し、改めて文字列型に直します。
        """
        err_st = eval( string.replace( e.msg, e_junk ,"" )).encode("utf-8")
        rpl_st = string.replace( err_st , "\"" , "" )
        rpl_st = string.replace( rpl_st , "\'" , "" )
        rpl_st = "\"%s\">" % string.replace( rpl_st, ">", "" )
        html = string.replace( html , err_st , rpl_st )
        sc =  get_yahoo_finance( html )
        return sc
    else :
        raise e
