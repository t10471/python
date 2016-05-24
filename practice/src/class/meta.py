# -*- coding: utf-8 -*-
from discripta import API
# from _pyio import __metaclass_

# __new__
# __init__より低レイヤーな初期化処理
# 継承先のクラスで明示的に呼ばなくても必ず基底の__new__は呼ばれる
class MetaKlass(object):

    def __new__(cls):
        # clsは継承先のクラスか、自クラスが設定される
        print('__new__ called')
        return object.__new__(cls)
    def __init__(self):
        print('__init__ called')
        self.a = 1

# __new__ called
# __init__ called
i  = MetaKlass()

class WithoutConstructor(MetaKlass):
    pass

# __new__ called
# __init__ called
i = WithoutConstructor()

class MyOtherMetaKlass(MetaKlass):

    def __init__(self):
        print('MyOtherMetaKlass __init__ called')
        super(MyOtherMetaKlass, self).__init__()
        self.b = 2

# __new__ called
# MyOtherMetaKlass __init__ called
# __init__ called
i = MyOtherMetaKlass()

def method(self):
    return 1

# class構文のシンタックスシュガー
klass = type('MClass', (object,), {'method': method})
i = klass()
print(i.method())

# classの場合は第一引数がメタクラスだが、関数の場合はない
# classの場合の引数metacls, cls_name, bases, attrs
def equip(cls_name, bases, attrs):
    print('cls_name', cls_name)
    print('bases', bases)
    print('attrs', attrs)
    if '__doc__' not in attrs:
        attrs['__doc__'] = API()
    return type(cls_name, bases, attrs)

class MMetaClass(object):
    # メタクラスはクラスではなくてもよい、
    # また結果はtypeの結果を返せばよい
    __metaclass__ = equip
    def alright(self):
        """the ok method"""
        return 'okay'
ma = MMetaClass()
print(ma.__class__)
print(ma.__class__.__dict__['__doc__'])
ma.y = 6
print(ma.__doc__)

# メタクラスを使わない方法
# 継承が複雑になるとメタクラスがつかいにくくなるので別の方法でクラスを拡張する方法
def enhancer_1(kklass):
    x = [l for l in kklass.__name__]
    # ['M', 'y', 'S', 'i', 'm', 'p', 'l', 'e', 'C', 'l', 'a', 's', 's']
    print(x)
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
    print(enhancers)
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
