# -*- coding: utf-8 -*-

from threading import Thread
import os
import subprocess
from Queue import Queue
import sys

dirname = os.path.realpath(os.path.dirname(__file__))
CONVERTER = os.path.join(dirname, 'converter.py')

#Queueはマルチスレッド
q = Queue()

def index_file(filename):
    f = open(filename)
    try:
        content = f.read()
        subprocess.call([CONVERTER, content])
    finally:
        f.close()

def worker():
    while True:
        index_file(q.get())
        #メインスレッドに処理が完了したことを通知
        q.task_done()

def index_files(files, num_workers):
    for i in  range(num_workers):
        t = Thread(target=worker)
        #メインスレッド時にワーカースレッドを終了する設定
        t.daemon = True
        t.start()
    for f in files:
        q.put(f)
    #全Queueが消費されるまで、待機
    q.join()

def get_text_files(dirname):
    for root, dirs, files in os.walk(dirname):
        for f in files:
            if os.path.splitext(f)[-1] != '.py':
                continue
        yield os.path.join(root, f)

def process(dirname, numthreads):
    dirname = os.path.realpath(dirname)
    print dirname
    if numthreads > 1:
        index_files(get_text_files(dirname), numthreads)
    else:
        for f in get_text_files(dirname):
            index_file(f)

if __name__ == '__main__':
    process(".", int(3))
