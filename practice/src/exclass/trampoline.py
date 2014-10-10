# -*- coding: utf-8 -*-

def demo_coroutine():
    """coroutine a la COBOL"""
    def coroutine_a(n = 0):
        while n < 10:
            n = yield b, n + 1
            print ">", n
    def coroutine_b(n = 0):
        while n < 10:
            n = yield a, n + 1
            print "<", n
    a = coroutine_a()
    b = coroutine_b()
    next(a)
    next(b)
    g = (a, 0)
    while True: # トランポリン
        try:
            g = g[0].send(g[1])
        except:
            break
if __name__ == '__main__':
    demo_coroutine()
