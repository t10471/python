# -*- coding: utf-8 -*-

import functools, inspect

def decorator(func):
    """ Allow to use decorator either with arguments or not. """
    print "decorator start"
    print func
    def isFuncArg(*args, **kw):
        #print isinstance(args[0], type)
        #classはtypeのインスタンス,詳しくはメタプログラミング
        ret = len(args) == 1 and len(kw) == 0 and (
            inspect.isfunction(args[0]) or isinstance(args[0], type))
        print "isFuncArg " + str(ret)
        print args
        print kw
        return ret

    print "isinstance(func, type) " + str(isinstance(func, type))
    print type(func)
#    <class '__main__.apply_class'>
#    isinstance(func, type) True
#    <type 'type'>
    #クラスの場合(objectを継承しているクラスはtype型)
    if isinstance(func, type):
        print 'class_wrapper'
        def class_wrapper(*args, **kw):
            #デコレータで引数を渡していない場合
            if isFuncArg(*args, **kw):
                return func()(*args, **kw) # create class before usage
            return func(*args, **kw)
        class_wrapper.__name__ = func.__name__
        class_wrapper.__module__ = func.__module__
        return class_wrapper

    print 'func_wrapper'
    @functools.wraps(func)
    def func_wrapper(*args, **kw):
        #デコレータで引数を渡していない場合
        if isFuncArg(*args, **kw):
            return func(*args, **kw)

        def functor(userFunc):
            print userFunc
            return func(userFunc, *args, **kw)

        return functor

    return func_wrapper

@decorator
def apply(func, *args, **kw): #@ReservedAssignment
    print "apply"
    return func(*args, **kw)

@apply
def test():
    return 'test'

assert test == 'test'

@apply(2, 3)
def test2(a, b):
    return a + b
assert test2 == 5

#この段階でclass_wrapperを作成
@decorator
class apply_class(object):
    def __init__(self, *args, **kw):
        print "apply_class __init__"
        print args
        print kw
        self.args = args
        self.kw   = kw

    def __call__(self, func):
        print "apply_class __call__"
        print func
        return func(*self.args, **self.kw)

#isFuncArg True
#apply_class __init__
#apply_class __call__
@apply_class
def test3():
    return 'test'

assert test3 == 'test'

#isFuncArg False
#apply_class __init__
#apply_class __call__
#この段階で処理は実行が完了してtest4に値が設定されている
@apply_class(2, 3)
def test4(a, b):
    return a + b

assert test4 == 5