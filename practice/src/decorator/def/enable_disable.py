# -*- coding: utf-8 -*-

def unchanged(func):
    "This decorator doesn't add any behavior"
    return func

def disabled(func):
    "This decorator disables the provided function, and does nothing"
    def empty_func(*args,**kargs):
        pass
    return empty_func

# define this as equivalent to unchanged, for nice symmetry with disabled
enabled = unchanged

#
# Sample use
#

global_enable_flag = True

state = enabled if global_enable_flag else disabled
@state
def special_function_foo():
    return "function was enabled"

print special_function_foo()

global_enable_flag = False

state = enabled if global_enable_flag else disabled
@state
def special_function_foo2():
    return "function was enabled"

print special_function_foo2()

print special_function_foo()
