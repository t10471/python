# -*- coding: utf-8 -*-

import time
import math
import random

# Retry decorator with exponential backoff
def retry(tries, delay=3, backoff=2):
    """Retries a function or method until it returns True.

    delay sets the initial delay in seconds, and backoff sets the factor by which
    the delay should lengthen after each failure. backoff must be greater than 1,
    or else it isn't really a backoff. tries must be at least 0, and delay
    greater than 0."""

    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")

    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay # make mutable

            rv = f(*args, **kwargs) # first attempt
            while mtries > 0:
                print mtries
                print mdelay

                if rv == True: # Done on success
                    return True

                mtries -= 1      # consume an attempt
                time.sleep(mdelay) # wait...
                mdelay *= backoff  # make future wait longer

                rv = f(*args, **kwargs) # Try again

            return False # Ran out of tries :-(

        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator

@retry(3,1,1.5)
def rand():
    rand = random.randint(0, 100)
    print "rand " + str(rand)
    if(rand < 10):
        return True
    return False

print rand()