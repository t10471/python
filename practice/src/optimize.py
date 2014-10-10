# -*- coding: utf-8 -*-

#リストの挿入
from bisect import bisect_left, bisect

#bisect_left,bisect挿入位置の検索
#bisectが右側bisect_leftが左側
seq = [2, 3, 7, 8, 9]
print bisect_left(seq, 5)
seq.insert(bisect_left(seq, 5), 5) #insort_left(seq, 5)と同じ
print bisect(seq, 5)
seq.insert(bisect(seq, 5), 5)
print seq

print bisect_left(seq, 7)
seq.insert(bisect_left(seq, 7), 7)
print bisect(seq, 7)
seq.insert(bisect(seq, 7), 7)
print seq

seq = [2, 3, 7, 8, 9]
def find (seq, el):
    pos = bisect_left(seq, el)
    print 'pos', pos
    if len(seq) == pos or seq[pos] != el:
        return -1
    return pos

print find(seq, 1)
print find(seq, 3)
print find(seq, 5)
print find(seq, 9)
print find(seq, 10)

#setが便利
seq = [1,2,3,5,5,6,7,7,9]
print set(seq)

#先頭や中間への挿入、削除はdequeのほうがスライスよりはやい
from collections import deque

my_list = range(10000)
my_deque = deque(my_list)

del my_list[500:502]
my_deque.rotate(500)
my_deque.pop()
my_deque.pop()
my_deque.rotate(-500)


#FIFOを実装するなら、listよりdeque
from collections import deque
import sys

queue = deque
def d_add_data(data):
    queue.appendleft(data)

def d_process_data():
    queue.pop()

BIG_N = 10000
def sequence():
    for i in range(BIG_N):
        d_add_data(i)
    for i in range(BIG_N/2):
        d_process_data()
    for i in range(BIG_N):
        d_add_data(i)

lqueue = []
def l_add_data(data):
    lqueue.insert(0, data)

def l_process_data():
    lqueue.pop()

#setdefaultより高速
from collections import defaultdict
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k,v in s:
    d[k].append(v)

print d.items()

#文字数のカウント
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1

print d.items()

import itertools

#初期化するのはcallableなものではなくてはいけない
def constant_factory(value):
    return itertools.repeat(value).next
print itertools.repeat('a').next() #a
d = defaultdict(constant_factory('<missing>'))
d.update(name='John', action='ran')

print d.items()

print '%(name)s %(action)s to %(object)s' % d