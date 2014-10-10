# -*- coding: utf-8 -*-
'''
Created on 2011/11/03

@author: tn10
'''
import exceptions
import multitask #@UnresolvedImport
from timeit import itertools
import itertools
from functools import wraps

def main():
    pass

#if __name__ == '__main__': main()


def _treatment(pos, element):
    return '%d: %s' % (pos, element)

seq = ["one", "two", "three"]
#リスト内包表記
res = [_treatment(pos, element) for pos, element in enumerate(seq)]
print res

#イテレータ
it = iter('abc')
for i in it:
    print i


#ジェネレータ#############
#yieldを返す関数は関数を実行したタイミングでは何も処理を行わない

def fibonasci():
    print "in"
    a, b = 0, 1
    while True:
        print "while 1"
        yield b
        a, b = b, a+b
        print "while 2"

#何も処理をしていないので in は表示されない
fib = fibonasci()
for i in range(5):
    print "for 1"
    #最初の呼び出しのタイミングで in が表示される
    #二回目の呼び出しで　while 2　が表示される
    print next(fib)
    print "for 2"
#ログ
#for 1
#in
#while 1
#1
#for 2
#for 1
#while 2
#while 1
#1
#for 2

#ret = [next(fib) for i in range(10)]
#print ret


def power(values):
    print "power", values
    for value in values:
        print('powering %s' % value)
        yield value * value

def adder(values):
    print "adder", values
    #valuesはpowerのジェネレータオブジェクト
    for value in values:
        print ('adding to %s' % value)
        if value % 2 == 0:
            yield value + 3
        else:
            yield value + 2


element = [i for i in range(10)]
res = adder(power(element))
print "res", res
for i in res:
    #遅延評価てきな? adder -> powerの順で呼び出される
    print i

#res <generator object adder at 0x00000000026AC090>
#adder <generator object power at 0x00000000026A0D38>
#power [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#powering 0
#adding to 0
#3

def psychologist():
    print('please tell me your problems')
    while True:
        answer = yield
        if answer is not None:
            if answer.endswith('?'):
                print ("Don't ask youself too much questions")
            elif 'good' in answer:
                print ("A that's good, go on")
            elif 'bad' in answer:
                print("don't be so negative" )

free = psychologist()
next(free)
while True:
    question = raw_input('Question :')
    if 'exit' or '' in question:
        break
    free.send(question)

def my_generator():
    try:
        yield 'something'
    except ValueError:
        yield 'dealing with the exception'
    finally:
        print("ok let's clean")
gen = my_generator()
print next(gen)
print gen.throw(ValueError('mean'))
gen.close

def coroutine_1():
    for i in range(3):
        print ('c1')
        yield i
def coroutine_2():
    for i in range(3):
        print ('c2')
        yield i

multitask.add(coroutine_1())
multitask.add(coroutine_2())
multitask.run()

#ジェネレータ式
#リスト内包表記を()でくくるとジェネレータ
iterer = (x ** 2 for x in range(10) if x % 2 == 0)
print iterer;
for el in iterer:
    print el


def string_at_five(strings):
    value = strings.strip()
    print value
    #特定のシーケンスへ移動
    for el in itertools.islice(value.split(), 4, None):
        yield el

itt = string_at_five("1 2 3 4 5 6 7 8")
print itt
print next(itt)
print "test"
for i in itt:
    print i

def with_head(iterable, headsize = 1):
    #イテレータをコピー
    a, b = itertools.tee(iterable)
    return list(itertools.islice(a, headsize)), b

seq = range(10)
print with_head(seq)
print with_head(seq, 4)
a,b = with_head(seq, 4)
for x in a:
    print x
for x in b:
    print x

def compress(data):
    return ((len(list(group)), name) for name, group in itertools.groupby(data))
def compress_ex(data):
    for name, group in itertools.groupby(data):
        print name, list(group)
def decompress(data):
    return (car * size for size, car in data)
def decompress_ex(data):
    for size, car in data:
        print car, size

test = "google"
compress_ex(test)
ret = compress(test)
r1, r2 = itertools.tee(ret)
r3, r4 = itertools.tee(r1)
print list(r2)
print ''.join(decompress(r3))
decompress_ex(r4)

a = 'google'
b = 'yahoo'
iterm = itertools.chain(a,b)
for i in iterm:
    print i
iterm = itertools.count(11)
for i in iterm:
    if i == 21:
        break
    print i

iterm = itertools.cycle(a)
for i,n in enumerate(iterm):
    if i == 21:
        break
    print n
L = [ "Marc Bolan", "David Bowie", "Mick Ronson",
   "Ian Hunter", "Morgan Fisher",
   "Brian Ferry", "Brian Eno", "Phil Manzanera", "Andy Mackay" ]
it = itertools.dropwhile(lambda item: item != 'Mick Ronson', L)
print list(it)

def mydecorator(function):
#    my_function.func_name
#    my_function.func_doc
#    を変更するためのデコレータ
    @wraps(function)
    def _mydecorator(*args, **kw):
        print "mydecorator pre"
        res = function(*args, **kw)
        print "mydecorator post"
        return res
    return _mydecorator

@mydecorator
def my_function(arg):

    """mydec"""
    print "my_function"
    return arg
#引数を渡すデコレータ
def mydecorator2(arg1, arg2):
    def _mydecorator(function):
        @wraps(function)
        def __mydecorator(*args, **kw):
            print "mydecorator2 pre"
            print arg1
            print arg2
            res = function(*args, **kw)
            print "mydecorator2 post"
            return res
        return __mydecorator
    return _mydecorator

@mydecorator2(1,2)
def my_function2(arg):
    """mydec"""
    print "my_function2"
    return arg

print my_function.func_name
print my_function.func_doc
my_function(1)
print my_function2.func_name
print my_function2.func_doc
my_function2(2)


def hoge(*args, **kwargs):
    foo(args, kwargs)
def foo(*args, **kwargs):
    print args
    print kwargs
def bar(*args, **kwargs):
    foo(*args, **kwargs)

hoge(1, 2, 3, ['a', 'b', 'c'], name='my_name', data='100')
bar(1, 2, 3, ['a', 'b', 'c'], name='my_name', data='100')
