# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, roles):
        self.roles = roles

class Unauthorized(Exception):
    pass

def protect(role):
    def _protect(function):
        def __protect(*args, **kw):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("I won't tell you")
            return function(*args, **kw)
        return __protect
    return _protect

if __name__ == '__main__':
    tarek = User(('admin', 'user'))
    bill = User(('user',))
    class MySecrets(object):
        @protect('admin')
        def waffle_recope(self):
            print ('use tons of butter')
    these_are = MySecrets()
    user = tarek
    these_are.waffle_recope()
    user = bill
    try:
        these_are.waffle_recope()
    except Unauthorized, e:
        print e

