# -*- coding: utf-8 -*-

#オブジェクトの生成だけを受け持つクラスを作成し、
#動的にオブジェクトを生成する
#生成されるオブジェクトは共通のAPIをもつ

from factory import Factory
import factory.list

import sys
if __name__ == '__main__':
    factory = Factory.getFactory('factory.list.ListFactory')
    asahi = factory.createLink("朝日新聞", "http://www.asahi.com/")
    yomiuri = factory.createLink("読売新聞", "http://www.yomiuri.co.jp/")
    us_yahoo = factory.createLink("Yahoo!", "http://www.yahoo.com/")
    jp_yahoo = factory.createLink("Yahoo!Japan", "http://www.yahoo.co.jp/")
    excite = factory.createLink("Exite", "http://www.excite.com/")
    google = factory.createLink("Google", "http://www.google.com/")

    traynews = factory.createTray("新聞")
    traynews.add(asahi)
    traynews.add(yomiuri)

    trayyahoo = factory.createTray("Yahoo!")
    trayyahoo.add(us_yahoo)
    trayyahoo.add(jp_yahoo)

    traysearch = factory.createTray("サーチエンジン")
    traysearch.add(trayyahoo)
    traysearch.add(excite)
    traysearch.add(google)

    page = factory.createPage("LinkPage", "name")
    page.add(traynews)
    page.add(traysearch)
    page.output()


#python abstract_factory_main.py listfactory.ListFactory
#python abstract_factory_main.py tablefactory.TableFactory