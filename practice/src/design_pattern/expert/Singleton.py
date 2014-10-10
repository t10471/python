# -*- coding: utf-8 -*-

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            print cls
            print orig
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            print cls._instance
        return cls._instance

class MyClass(Singleton):
    a = 1
    def __init__(self):
        self.b = 2
        print "__init__"

one = MyClass()
two = MyClass()

print one.a,two.a

two.a = 10

print one.a,two.a

print one.b,two.b

two.b = 20

print one.b,two.b

print '++++++++++++++++++'

#__dict__を使って共有する
class Borg(object):
    _state = {}
    def __new__(cls, *args, **kwargs):
        ob = super(Borg, cls).__new__(cls, *args, **kwargs)
        #pythonは参照渡しのため、参照を変えている
        ob.__dict__ = cls._state
    #<__main__.MyBorg object at 0x0000000002273400> <class '__main__.MyBorg'> {}
    #<__main__.MyBorg object at 0x0000000002273438> <class '__main__.MyBorg'> {'x': 3}
    #<__main__.MyOtherBorg object at 0x0000000002273470> <class '__main__.MyOtherBorg'> {'x': 3}
    #<__main__.MyOtherBorg object at 0x00000000022734A8> <class '__main__.MyOtherBorg'> {'x': 3}
        print ob, cls, ob.__dict__
        return ob

class MyBorg(Borg):
    a = 1
    def __init__(self):
        self.x = 3
    def meth(self):
        return self.x * 10

class MyOtherBorg(MyBorg):
    b = 2
    def __init__(self):
        super(MyOtherBorg, self).__init__()
    def meth(self):
        return self.x * 10
    def mod(self):
        self.x = 4

one = MyBorg()
two = MyBorg()
three = MyOtherBorg()
four = MyOtherBorg()

#1 1 1 1
print one.a, two.a, three.a, four.a
two.a = 10
#10 10 10 10
print one.a, two.a, three.a, four.a
#30 30
print one.meth(), four.meth()
three.mod()

#40 40
print one.meth(), four.meth()

#まだ、どの__dict__にもbは存在しない
#{'a': 10, 'x': 4} {'a': 10, 'x': 4} {'a': 10, 'x': 4} {'a': 10, 'x': 4}
print one.__dict__, two.__dict__, three.__dict__, four.__dict__

#実行することで、すべての__dict__に存在する
#2 2
print three.b, four.b
three.b = 20
#20 20
print three.b, four.b
#{'a': 10, 'x': 4, 'b': 20} {'a': 10, 'x': 4, 'b': 20} {'a': 10, 'x': 4, 'b': 20} {'a': 10, 'x': 4, 'b': 20}
print one.__dict__, two.__dict__, three.__dict__, four.__dict__
#['_state', 'a', 'b', 'meth', 'x'] ['_state', 'a', 'b', 'meth', 'mod', 'x']
print  filter(lambda x: not x.startswith('__'), dir(one)), filter(lambda x: not x.startswith('__'), dir(three))

#パッケージはsingleton
a = 100
import single
s = single
print single.a , s.a
#aを変更
s.modA(10) #single.a = 10と変わらない
a = 1000
print single.a , s.a
