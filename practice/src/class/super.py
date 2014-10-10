# -*- coding: utf-8 -*-

class Mama(object):
    def says(self):
        print("do your homework")

class Sister(Mama):
    def says(self):
        #親のオブジェクトを取得
        #厳密にはちがうが
        super(Sister, self).says()
        print('and clean your bedroom')

anita = Sister()
anita.says()

#MROメソッド解決順序

class A(object):
    def __init__(self):
        print("A")
        print super(A, self)
        super(A, self).__init__()

class B(object):
    def __init__(self):
        print("B")
        print super(B, self)
        super(B, self).__init__()


class C(A, B):
    def __init__(self):
        print("C")
        super(C, self).__init__()

        #別々に呼ぶとCABBとなる
        #A.__init__(self)
        #B.__init__(self)


C()
print('+++++++++++++')
A()