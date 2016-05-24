# -*- coding: utf-8 -*-

class PrototypeStore(dict):

    def __init__(self):
        print('PrototypeStore __init__')

    """ x.prototype.XXXの値を保存するためのクラス """
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

class PrototypeMeta(type):

    def __init__(self, cls_name, bases, attrs):
        print('PrototypeMeta __init__')

    """ Prototypeメタクラス(クラス生成時に呼ばれる) """
    # typeクラスの__new__,__init__と引数の型を同じにする必要がある
    # そもそも__init__と__new__の引数は一緒
    # __new__で返したクラスのインスタンスが__init__のselfになる

    def __new__(metacls, cls_name, bases, attrs):

        # __metaclass__で呼ばれた場合の第一引数は自クラス
        print('in PrototypeMeta __new__')
        print('  metacls', metacls)
        print('  cls_name', cls_name)
        print('  bases', bases)
        print('  attrs', attrs)

        cls = type.__new__(metacls, cls_name, bases, attrs)
        print('  cls', cls)
        cls.prototype = PrototypeStore()
        return cls

# クラスの宣言時にメタクラスの処理が走るs
# metacls <class '__main__.PrototypeMeta'>
# cls_name Prototype
# bases (<type 'object'>,)
# attrs {'__module__': '__main__', '__metaclass__': <class '__main__.PrototypeMeta'>, '__getattr__': <function __getattr__ at 0x00000000025B1F28>}
# cls <class '__main__.Prototype'>
class Prototype(object, metaclass=PrototypeMeta):
    # python3では意味なし上の宣言のみ通用する
    # __metaclass__ = PrototypeMeta

    def __init__(self):
        print('Prototype __init__')

    def __getattr__(self, name):
        if name == 'prototype':
            getattr(self.__class__, name)
        else:
            try:
                getattr(object, name)
            except AttributeError:
                return self.__class__.prototype[name]

# もう一度メタクラスの処理が走る
# metacls <class '__main__.PrototypeMeta'>
# cls_name TestClass
# bases (<class '__main__.Prototype'>,)
# attrs {'__module__': '__main__', '__init__': <function __init__ at 0x00000000025B1F98>}
# cls <class '__main__.TestClass'>
# TestClass __init__
class TestClass(Prototype):

    def __init__(self):
        print("TestClass __init__")
        pass

if __name__ == '__main__':
    print('first create')
    first = TestClass()
    first.prototype.x = 7
    print('second create')
    second = TestClass()
    print(second.x)        # first.xと同じオブジェクトを指しているので7になる
    first.x = 9            # first(インスタンス)の'x'アトリビュートに代入
    print(first.x)         # これは7でなく9を返す
    del first.x            # インスタンスのアトリビュートを消去
    print(first.x)         # prototype.xの返す7になるはず
