# -*- coding: utf-8 -*-

def dump_args(func):
    "This decorator dumps out the arguments passed to a function before calling it"
    #関数の変数名を取得
    #print func.func_code.co_varnames
    #関数の引数の数を取得
    #print func.func_code.co_argcount
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    def echo_func(*args,**kwargs):
        print fname, ":", ', '.join(
            '%s=%r' % entry
            for entry in zip(argnames,args) + kwargs.items())
        return func(*args, **kwargs)
    return echo_func

@dump_args
def f1(a,b,c):
    print a + b + c

f1(1, 2, 3)