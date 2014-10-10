# -*- coding: utf-8 -*-

"""
Allows you to test unimplemented code in a development environment
by specifying a default argument as an argument
to the decorator (or you can leave it off to specify None to be returned.
"""
# Annotation wrapper annotation method
def unimplemented(defaultval):
    print type(unimplemented)
    print type(defaultval)
    if(type(defaultval) == type(unimplemented)):
        def f(func):
            print func
            return func
        return f
        #return lambda : None
    else:
        # Actual annotation
        def unimp_wrapper(func):
            print func
            # What we replace the function with
            def wrapper(*arg):
                return defaultval
            return wrapper
        return unimp_wrapper

def implemented(func):
    print func
    return func

@unimplemented("implemented")
@implemented
def funcc(i):
    return i

@unimplemented(unimplemented)
@implemented
def funcc2(i):
    return i

print funcc(2)
print funcc2(2)
