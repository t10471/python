# -*- coding: utf-8 -*-

with file('echo.py') as hosts:
    for line in hosts:
        if line.startswith('#'):
            continue
        print line

#withを実装するプロトコル
class Context(object):
    def __enter__(self):
        print 'entering the zone'
        #asで渡す値を返す
        return self
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None:
            print 'with no error'
        else:
            print 'with an error (%s)' % exception_value
            #Trueを返すと例外が外に伝わらない
            #return True

print ('class')
with Context() as const:
    print const
    print 'i am zone'

try:
    with Context():
        print 'i am the buggy zone'
        raise TypeError('i am the bug')
except Exception as e:
    pass

from contextlib import contextmanager, closing
import urllib

#class Contextと同様の機能をデコレータで実装
@contextmanager
def context():
    print('entering the zone')
    try:
        yield
    except Exception as e:
        print('with an error (%s)' % e)
        raise e
    else:
        print('with no error')

print ('function')
with context() as const:
    #Noneがかえってくる
    print const
    print 'i am zone'

try:
    with context():
        print 'i am the buggy zone'
        raise TypeError('i am the bug')
except Exception as e:
    pass

#urllib.urlopen('http://www.python.org')
#は__exit__メソッドを実装していないが
#closeingを適用するとcontextmanagerでデコレートしたものになるのでwithが使える
with closing(urllib.urlopen('http://www.python.org')) as page:
    for line in page:
        print line

fp = urllib.urlopen('http://www.python.org')
print fp
fp.close()


#withのネスト
#with A() as a, B() as b:
#    suite
#は、以下と同等です:
#
#with A() as a:
#    with B() as b:
#        suite