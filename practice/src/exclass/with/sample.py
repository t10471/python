# -*- coding: utf-8 -*-

from contextlib import contextmanager

#class Contextと同様の機能をデコレータで実装
@contextmanager
def logged(klass, logger):
    #ロガー
    def _log(f):
        def __log(*args, **kw):
            logger(f, args, kw)
            return f(*args, **kw)
        return __log

    for attribute in dir(klass):
        if attribute.startswith('_'):
            continue
        element = getattr(klass, attribute)

        #元のメソッドをバックアップ
        setattr(klass, '__logged_%s' % attribute, element)
        #ログつきメソッドに変更
        setattr(klass, attribute, _log(element))

    print dir(klass)
    #ここまでがwithステートメントで実行される
    yield klass
    #ここからがwithブロックを抜けるときに実行される
    #yieldした値は __enter__メソッドの戻り値となる

    #追加したログ取得用のオブジェクトを削除
    for attribute in dir(klass):
        #変更したメソッドのみ抽出
        if not attribute.startswith('__logged_'):
            continue
        element = getattr(klass, attribute)
        setattr(klass, attribute[len('__logged_'):], element)
        delattr(klass, attribute)

    print dir(klass)

class One(object):
    def _private(self):
        pass
    def one(self, other):
        self.two()
        other.thing(self)
        self._private()
    def two(self):
        pass

class Two(object):
    def thing(self, other):
        other.two()

calls = []

def called(meth, args, kw):
    calls.append(meth.im_func.func_name)

print 1
with logged(One, called):
    print 2
    one = One()
    two = Two()
    one.one(two)
print 3

print calls