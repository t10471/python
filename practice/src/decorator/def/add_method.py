# -*- coding: utf-8 -*-

class Foo:
    def __init__(self):
        self.x = 42

foo = Foo()

def addto(instance):
    def decorator(f):
        import types
        #fというメソッドをinstance.__class__型のinstanceに作成する
        #ただしfはメソッド
        f = types.MethodType(f, instance, instance.__class__)
        #fooインスタンスにfを設定
        setattr(instance, f.func_name, f)
        return f
    return decorator

@addto(foo)
def print_x(self):
    #setattrしているから、メソッドになるのでselfがついてくる
    print self.x

print_x()
foo.print_x()