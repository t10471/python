# -*- coding: utf-8 -*-

#fork

#import os
#
#a = []
#
#def some_work():
#    a.append(2)
#
#child_pid = os.fork()
#
#if child_pid == 0:
#    a.append(3)
#    print("hey, I am the child process")
#    print("I'm pid is %d" % os.getpid())
#    print( str(a))
#else:
#    a.append(4)
#    print("hey, I am the parent")
#    print("the child  pid is %d" % child_pid)
#    print("I'm pid is %d" % os.getpid())
#    print( str(a))
#
#if __name__ == '__main__':
#    some_work()

#multiprocessing

#from multiprocessing import Process
#import time
#import os
#
#def work():
#    print('hey i am a process, id: %d' % os.getpid())
#
#print os.getpid()
#ps = []
#for i in range(4):
#    p = Process(target=work)
#    ps.append(p)
#    p.start()
#
#print(ps)
#time.sleep(1)
#print(ps)
#
#for p in ps:
#    p.join()

#pool

import multiprocessing
import Queue
import os

print('this michine has %d CPUs' % multiprocessing.cpu_count())

def worker():
    f = q.get_nowait()
    return 'work on ' + f + ' in ' + str(os.getpid())


if __name__ == '__main__':

    q = multiprocessing.Queue()
    pool = multiprocessing.Pool()

    for i in ('f1', 'f2', 'f3', 'f4', 'f5'):
        q.put(i)

    print os.getpid()

    while True:
        try:
            #multiprocessing.pool.ApplyResult
            #デフォルトでCPU分のプロセスを生成
            result = pool.apply_async(worker)
            print result
            print result.get(timeout=1)

        except Queue.Empty:
            break

