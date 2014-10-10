# -*- coding: utf-8 -*-

"""
Provide pre-/postconditions as function decorators.

Example usage:

  >>> def in_ge20(inval):
  ...    assert inval >= 20, 'Input value < 20'
  ...
  >>> def out_lt30(retval, inval):
  ...    assert retval < 30, 'Return value >= 30'
  ...
  >>> @precondition(in_ge20)
  ... @postcondition(out_lt30)
  ... def inc(value):
  ...   return value + 1
  ...
  >>> inc(5)
  Traceback (most recent call last):
    ...
  AssertionError: Input value < 20
  >>> inc(29)
  Traceback (most recent call last):
    ...
  AssertionError: Return value >= 30
  >>> inc(20)
  21

You can define as many pre-/postconditions for a function as you
like. It is also possible to specify both types of conditions at once:

  >>> @conditions(in_ge20, out_lt30)
  ... def add1(value):
  ...   return value + 1
  ...
  >>> add1(5)
  Traceback (most recent call last):
    ...
  AssertionError: Input value < 20

An interesting feature is the ability to prevent the creation of
pre-/postconditions at function definition time. This makes it
possible to use conditions for debugging and then switch them off for
distribution.

  >>> debug = False
  >>> @precondition(in_ge20, debug)
  ... def dec(value):
  ...   return value - 1
  ...
  >>> dec(5)
  4
"""

__all__ = ['precondition', 'postcondition', 'conditions']

DEFAULT_ON = True

def precondition(precondition, use_conditions=DEFAULT_ON):
    return conditions(precondition, None, use_conditions)

def postcondition(postcondition, use_conditions=DEFAULT_ON):
    return conditions(None, postcondition, use_conditions)

class conditions(object):
    __slots__ = ('__precondition', '__postcondition')

    def __init__(self, pre, post, use_conditions=DEFAULT_ON):
        print "conditions __init__", self
        if not use_conditions:
            pre, post = None, None

        self.__precondition  = pre
        self.__postcondition = post

    def __call__(self, function):
        #functionは最初に呼ばれるたデコレータのときはdefだが、
        #2個目以降はFunctionWrapperのオブジェクト
        print "conditions __call__", function, self
        # combine recursive wrappers (@precondition + @postcondition == @conditions)
        pres  = set((self.__precondition,))
        posts = set((self.__postcondition,))

        #print "hasattr(function, '__iter__')", hasattr(function, '__iter__') 常にFalse
        # unwrap function, collect distinct pre-/post conditions
        #functionは再帰になっているからwhileが使える?
        while function:
            print "while", function
            if type(function) is FunctionWrapper:
                pres.add(function._pre)
                posts.add(function._post)
                function = function._func
            else:
                break

        # filter out None conditions and build pairs of pre- and postconditions
        #map(None,,)でzipと一緒
        conditions = map(None, filter(None, pres), filter(None, posts))
        print "conditions", conditions

        # add a wrapper for each pair (note that 'conditions' may be empty)
        #functionを再帰的に設定
        #whileで進めているため必ずfuncionにはデコレーション対象の関数が設定されている
        for pre, post in conditions:
            print "for funtion ", function
            function = FunctionWrapper(pre, post, function)
        print "function", function

        return function

class FunctionWrapper(object):
    def __init__(self, precondition, postcondition, function):
        print "FunctionWrapper __init__", self, precondition, postcondition
        self._pre  = precondition
        self._post = postcondition
        self._func = function

    def __call__(self, *args, **kwargs):
        precondition  = self._pre
        postcondition = self._post
        print "FunctionWrapper __call__",self , precondition, postcondition
        if precondition:
            precondition(*args, **kwargs)
        print self._func
        result = self._func(*args, **kwargs)
        if postcondition:
            postcondition(result, *args, **kwargs)
        return result

#def __test():
#    import doctest
#    doctest.testmod()

if __name__ == "__main__":
    def in_ge20(inval):
        print "in_ge20", inval
        return 20 + inval
        return inval
    def in_ge21(inval):
        print "in_ge21", inval
        return 21 + inval
        return inval
#    def in_ge22(inval):
#        print "in_ge22", inval
#        return 22 + inval
#        return inval
    def out_lt30(retval, inval):
        print "out_lt30",retval, inval
        return 30 + retval
    def out_lt31(retval, inval):
        print "out_lt31",retval, inval
        return 31 + retval
#    def out_lt32(retval, inval):
#        print "out_lt32",retval, inval
#        return 32 + retval

    #引数のあるクラスデコレータは先に__call__が呼ばれる
    @precondition(in_ge20)
    @precondition(in_ge21)
#    @precondition(in_ge22)
    @postcondition(out_lt30)
    @postcondition(out_lt31)
#    @postcondition(out_lt32)
    def inc(value):
        print "inc", value
        return value + 1
    print inc(5)
#    inc(29)
#    inc(20)

"""
conditions __init__ <conditions #obj1>
conditions __init__ <conditions #obj2>
conditions __init__ <conditions #obj3>
conditions __init__ <conditions #obj4>

#下のデコレータから処理開始
conditions __call__ < inc > <conditions #obj4>
while < inc >
conditions [(None, < out_lt31 >)]
for funtion  < inc >
FunctionWrapper __init__ <Wrapper #obj5> None < out_lt31 >
function <Wrapper #obj5>

conditions __call__ <Wrapper #obj5> <conditions #obj3>
#functionには前の戻り値が設定されている
while <Wrapper #obj5>
while < inc >
conditions [(None, < out_lt31 >), (None, < out_lt30 >)]
for funtion  < inc >
FunctionWrapper __init__ <Wrapper #obj6> None < out_lt31 >
for funtion  <Wrapper #obj6>
FunctionWrapper __init__ <Wrapper #obj7> None < out_lt30 >
function <Wrapper #obj7>

conditions __call__ <Wrapper #obj7> <conditions #obj2>
while <Wrapper #obj7>
while <Wrapper #obj6>
while < inc >
conditions [(< in_ge21 >, < out_lt31 >), (None, < out_lt30 >)]
for funtion  < inc >
FunctionWrapper __init__ <Wrapper #obj3> < in_ge21 > < out_lt31 >
for funtion  <Wrapper #obj3>
FunctionWrapper __init__ <Wrapper #obj4> None < out_lt30 >
function <Wrapper #obj4>

conditions __call__ <Wrapper #obj4> <conditions #obj1>
while <Wrapper #obj4>
while <Wrapper #obj3>
while < inc >
conditions [(< in_ge20 >, < out_lt31 >), (< in_ge21 >, < out_lt30 >)]
#再帰的にfunctionを設定
for funtion  < inc >
FunctionWrapper __init__ <Wrapper #obj7> < in_ge20 > < out_lt31 >
for funtion  <Wrapper #obj7>
FunctionWrapper __init__ <Wrapper #obj6> < in_ge21 > < out_lt30 >
function <Wrapper #obj6>

FunctionWrapper __call__ <Wrapper #obj6> < in_ge21 > < out_lt30 >
#最初のデコレータが処理される
in_ge21 5

#_funcが実行される
<Wrapper #obj7>
FunctionWrapper __call__ <Wrapper #obj7> < in_ge20 > < out_lt31 >
in_ge20 5

< inc >
inc 5
out_lt31 6 5
out_lt30 6 5
6
"""

#    @conditions(in_ge20, out_lt30)
#    def add1(value):
#        return value + 1
#    add1(5)
#    debug = False
#    @precondition(in_ge20, debug)
#    def dec(value):
#        return value - 1
#    dec(5)
