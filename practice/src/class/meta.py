# -*- coding: utf-8 -*-
from discripta import API
from _pyio import __metaclass__

#__new__
#__init__より低レイヤーな初期化処理
#継承先のクラスで明示的に呼ばなくても必ず基底の__new__は呼ばれる
class MetaKlass(object):
    def __new__(cls):
        #clsは継承先のクラスか、自クラスが設定される
        print('__new__ called')
        return object.__new__(cls)
    def __init__(self):
        print('__init__ called')
        self.a = 1

#__new__ called
#__init__ called
i  = MetaKlass()

class WithoutConstructor(MetaKlass):
    pass

#__new__ called
#__init__ called
i = WithoutConstructor()

class MyOtherMetaKlass(MetaKlass):
    def __init__(self):
        print('MyOtherMetaKlass __init__ called')
        super(MyOtherMetaKlass, self).__init__()
        self.b = 2

#__new__ called
#MyOtherMetaKlass __init__ called
#__init__ called
i = MyOtherMetaKlass()

def method(self):
    return 1

#class構文のシンタックスシュガー
klass = type('MClass', (object,), {'method': method})
i = klass()
print i.method()

## -*- coding: utf-8 -*-

class PrototypeStore(dict):
    """ x.prototype.XXXの値を保存するためのクラス """
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

class PrototypeMeta(type):
    """ Prototypeメタクラス(クラス生成時に呼ばれる) """
    #typeクラスの__new__,__init__と引数の型を同じにする必要がある
    #そもそも__init__と__new__の引数は一緒
    #__new__で返したクラスのインスタンスが__init__のselfになる
    def __new__(metacls, cls_name, bases, attrs): #@NoSelf
        #__metaclass__で呼ばれた場合の第一引数は自クラス
        print 'metacls', metacls
        print 'cls_name', cls_name
        print 'bases', bases
        print 'attrs', attrs
        #type('MClass', (object,), {'method': method})

        cls = type.__new__(metacls, cls_name, bases, attrs)
        print 'cls', cls
        cls.prototype = PrototypeStore()
        return cls

#クラスの宣言時にメタクラスの処理が走るs
#metacls <class '__main__.PrototypeMeta'>
#cls_name Prototype
#bases (<type 'object'>,)
#attrs {'__module__': '__main__', '__metaclass__': <class '__main__.PrototypeMeta'>, '__getattr__': <function __getattr__ at 0x00000000025B1F28>}
#cls <class '__main__.Prototype'>
class Prototype(object):
    __metaclass__ = PrototypeMeta

    def __getattr__(self, name):
        if name == 'prototype':
            getattr(self.__class__, name)
        else:
            try:
                getattr(object, name)
            except AttributeError:
                return self.__class__.prototype[name]

#metacls <class '__main__.PrototypeMeta'>
#cls_name TestClass
#bases (<class '__main__.Prototype'>,)
#attrs {'__module__': '__main__', '__init__': <function __init__ at 0x00000000025B1F98>}
#cls <class '__main__.TestClass'>
#TestClass __init__
class TestClass(Prototype):
    def __init__(self):
        print "TestClass __init__"
        pass


first = TestClass() # オブジェクトを作る
first.prototype.x = 7 # 'x'をprototypeに割り当てる
second = TestClass() # firstと同じTextClassからインスタンスを作る
print second.x # first.xと同じオブジェクトを指しているので7になる
first.x = 9 # first(インスタンス)の'x'アトリビュートに代入
print first.x # これは7でなく9を返す
del first.x # インスタンスのアトリビュートを消去
print first.x # prototype.xの返す7になるはず

#classの場合は第一引数がメタクラスだが、関数の場合はない
#classの場合の引数metacls, cls_name, bases, attrs
def equip(cls_name, bases, attrs):
    print 'cls_name', cls_name
    print 'bases', bases
    print 'attrs', attrs
    if '__doc__' not in attrs:
        attrs['__doc__'] = API()
    return type(cls_name, bases, attrs)
class MMetaClass(object):
    #メタクラスはクラスではなくてもよい、
    #また結果はtypeの結果を返せばよい
    __metaclass__ = equip
    def alright(self):
        """the ok method"""
        return 'okay'
ma = MMetaClass()
print ma.__class__
print ma.__class__.__dict__['__doc__']
ma.y = 6
print(ma.__doc__)

#メタクラスを使わない方法
#継承が複雑になるとメタクラスがつかいにくくなるので別の方法でクラスを拡張する方法
def enhancer_1(kklass):
    x = [l for l in kklass.__name__ ]
    #['M', 'y', 'S', 'i', 'm', 'p', 'l', 'e', 'C', 'l', 'a', 's', 's']
    print x
    c = [l for l in kklass.__name__ if l.isupper()]
    kklass.contracted_name = ''.join(c)

def enhancer_2(kklass):
    def logger(function):
        def wrap(*args, **kw):
            print('I log everything !')
            return function(*args, **kw)
        return wrap
    for el in dir(kklass):
        if el.startswith('?'):
            continue
        value = getattr(kklass, el)
        if not hasattr(value, 'im_func'):
            continue
        setattr(kklass, el, logger(value))

def enhance(kklass, *enhancers):
    print enhancers
    for enhancer in enhancers:
        enhancer(kklass)


class MySimpleClass(object):
    def ok(self):
        """i return ok"""
        return 'I lied'
enhance(MySimpleClass, enhancer_1, enhancer_2)
thats = MySimpleClass()
print(thats.ok())
print(thats.contracted_name)
