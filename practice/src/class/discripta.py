# -*- coding: utf-8 -*-


# ディスクリプタクラス
class UpperString(object):

    def __init__(self):
        self._value = ''
    def __get__(self, instance, klass):
        return self._value
    def __set__(self, instance, value):
        self._value = value.upper()

class MyClass(object):
    attribute = UpperString()

def smple1():
    instance_of = MyClass()

    # ディスクリプタかどうか判断して。違ったら、その後に__dict__を調べる
    print(instance_of.attribute)
    instance_of.attribute = 'my value'
    print(instance_of.attribute)
    # __dict__は空
    print(instance_of.__dict__)

    instance_of._new_attr = 1
    # {'_new_attr': 1}
    print(instance_of.__dict__)

    MyClass.new_attr = UpperString()
    # {'_new_attr': 1}
    print(instance_of.__dict__)
    print(instance_of.new_attr)

    instance_of.new_attr = 'other_value'
    print(instance_of.new_attr)
    # {'_new_attr': 1}のまま
    print(instance_of.__dict__)

# インロトスペクションディスクリプタ
# 状態をデバッグできる
# APIディスクリプタが別のクラスの状態を返す
class API(object):

    def _print_values(self, obj):
        def _print_value(key):
            if key.startswith('_'):
                return ''
            # valueはメソッドかプロパティ
            # Pythonで動的にメソッドを取得する
            value = getattr(obj, key)
            # python3ではim_func が__func__
            # メソッドはim_func im_class im_selfをもっている
            if not hasattr(value, 'im_func'):
                doc = type(value).__name__
            else:
                if value.__doc__ is None:
                    doc = 'no docstring'
                else:
                    doc = value.__doc__
            return '  %s : %s' % (key, doc)
        res = [_print_value(el) for el in dir(obj)]
        return '\n'.join([el for el in res if el != ''])

    def __get__(self, instance, klass):
        if instance is not None:
            return self._print_values(instance)
        else:
            return self._print_values(klass)
class MClass(object):
    __doc__ = API()  # @ReservedAssignment
    def __init__(self):
        self.a = 2

    def meth(self):
        """my method"""
        return 1

def sample2():
    print(MClass.__doc__)
    instance = MClass()
    print(instance.__doc__)


# メタディスクリプタ
# ディスクリプタを外から渡し、メソッドを合成する
class Chainer(object):

    def __init__(self, methods, callback=None):
        self._methods = methods
        self._callback = callback
    def __get__(self, instance, klass):
        if instance is None:
            # インスタンスにしか動作しない
            return self
        results = []
        for method in self._methods:
            results.append(method(instance))
            if self._callback is not None:
                if not self._callback(instance, method, results):
                    break
        return results

class TextProcessor(object):

    def __init__(self, text):
        self.text = text
    def normalize(self):
        if isinstance(self.text, list):
            self.text = [t.lower() for t in self.text]
        else:
            self.text = self.text.lower()
    def split(self):
        if not isinstance(self.text, list):
            self.text = self.text.split()
    def treshold(self):
        if not isinstance(self.text, list):
            if len(self.text) < 2:
                self.text = ''
        self.text = [w for w in self.text if len(w) > 2]

def logger(instance, method, results):
    print('calling %s' % method.__name__)
    return True
def add_sequence(name, sequence):
    # TextProcessorにnameというsequenceには行っているメソッドをチェインするメソッドを定義
    setattr(TextProcessor, name, Chainer([getattr(TextProcessor, n) for n in sequence], logger))

def sample3():
    add_sequence('simple_clean', ('split', 'treshold'))
    my = TextProcessor(' My Tylor is Rich')
    print(my.simple_clean)

    print(my.text)
    add_sequence('full_work', ('normalize', 'split', 'treshold'))
    print(my.full_work)
    print(my.text)

# プロパティ
class PropertyClass(object):

    def __init__(self):
        self._my_sercret_thing = 1

    def _i_get(self):
        return self._my_sercret_thing
    def _i_set(self, value):
        self._my_sercret_thing = value
    def _i_del(self):
        print('neh!')

    my_thing = property(_i_get, _i_set, _i_del, 'the thing')

def sample4():
    instance_of = PropertyClass()
    print(instance_of.my_thing)

    instance_of.my_thing = 3
    print(instance_of.my_thing)

    del instance_of.my_thing

    print(help(instance_of))

class FirstClass(object):

    def _get_price(self):
        return '$ 500'
    # _get_the_priceに値を設定する処理を書くと
    # オーバーライドできないため一つかます
    def _get_the_price(self):
        return self._get_price()
    price = property(_get_the_price)

class SecondClass(FirstClass):

    def _get_price(self):
        return '$ 20'

def sample5():
    ticket = SecondClass()
    print(ticket.price)


# スロット
# 指定した属性しかもてない
class Frozen(object):
    __slots__ = ['ice', 'cream']

def sample6():
    # false
    print('__dict__' in dir(Frozen))
    print(dir(Frozen))
    fr = Frozen()
    try:
        fr.icey = 1
    except AttributeError as e:
        print(e)
