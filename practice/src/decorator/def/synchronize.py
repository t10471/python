# -*- coding: utf-8 -*-

def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap

# Example usage:

from threading import Lock
my_lock = Lock()

@synchronized(my_lock)
def critical1(*args):
    # Interesting stuff goes here.
    pass

@synchronized(my_lock)
def critical2(*args):
    # Other interesting stuff goes here.
    pass