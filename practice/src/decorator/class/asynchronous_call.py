# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
import sys

class asynchronous(object):
    def __init__(self, func):
        print self.__class__, sys._getframe().f_code.co_name
        self.func = func

        def threaded(*args, **kwargs):
            print sys._getframe().f_code.co_name
            self.queue.put(self.func(*args, **kwargs))

        self.threaded = threaded
    #サンプルでは呼び出されない
    def __call__(self, *args, **kwargs):
        print self.__class__, sys._getframe().f_code.co_name
        return self.func(*args, **kwargs)

    def start(self, *args, **kwargs):
        print self.__class__, sys._getframe().f_code.co_name
        self.queue = Queue()
        thread = Thread(target = self.threaded, args = args, kwargs = kwargs);
        thread.start();
        return asynchronous.Result(self.queue, thread)

    class NotYetDoneException(Exception):
        def __init__(self, message):
            self.message = message

    class Result(object):
        def __init__(self, queue, thread):
            print self.__class__, sys._getframe().f_code.co_name
            self.queue = queue
            self.thread = thread

        def is_done(self):
            print self.__class__, sys._getframe().f_code.co_name
            return not self.thread.is_alive()

        def get_result(self):
            print self.__class__, sys._getframe().f_code.co_name
            if not self.is_done():
                raise asynchronous.NotYetDoneException('the call has not yet completed its task')

            if not hasattr(self, 'result'):
                self.result = self.queue.get()

            return self.result

if __name__ == '__main__':
    # sample usage
    import time

    print "asynchronous"
    #__init__だけ呼ばれる
    @asynchronous
    def long_process(num):
        print sys._getframe().f_code.co_name
        time.sleep(10)
        return num * num

    print "result"
    result = long_process.start(12)

    for i in range(20):
        print i
        time.sleep(1)

        if result.is_done():
            print "result {0}".format(result.get_result())


    print "result2"
    result2 = long_process.start(13)

    try:
        #終了していないので例外
        print "result2 {0}".format(result2.get_result())

    except asynchronous.NotYetDoneException as ex:
        print ex.message