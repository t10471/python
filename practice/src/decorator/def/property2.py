# -*- coding: utf-8 -*-

#import sys
#
#def traceit(frame, event, arg):
#    print event
#    if event == "line":
#        lineno = frame.f_lineno
#        print "line", lineno
#
#    return traceit
#
#def main():
#    print "In main"
#    for i in range(5):
#        print i, i*3
#    print "Done."
#
#関数のトレースを行うメソッド
#sys.settrace(traceit)
#main()

#ctr + 1で警告を非表示
"""
フレーム (frame) オブジェクト
  フレームオブジェクトは実行フレーム (execution frame)
  を表します。実行フレームはトレースバックオブジェクト内に出現します (下記参照)。

読み出し専用の特殊属性:
f_back は (呼び出し側にとっての) 以前のスタックフレームです。
  呼び出し側がスタックフレームの最下段である場合には None です;
f_code は現在のフレームで実行しようとしているコードオブジェクトです;
f_locals はローカル変数を検索するために使われる辞書です;
f_globals はグローバル変数用です;
f_builtins は組み込みの (Python 固有の) 名前です;
f_restricted は、関数が制限つき実行 (restricted execution) モードで実行されているかどうかを示すフラグです;
f_lasti は厳密な命令コード (コードオブジェクト中のバイトコード文字列へのインデクス) です。

書き込み可能な特殊属性:
f_trace が None でない場合、各ソースコード行の先頭で呼び出される関数になります;
f_exc_type, f_exc_value, f_exc_traceback は、現在のフレームが以前に引き起こした例外が
  提供する親フレーム内でもっとも最近捕捉された例外を表します (それ以外の場合は、これらはNoneになります。);
f_lineno はフレーム中における現在の行番号です — トレース関数 (trace function) 側でこの値に書き込みを行うと、
  指定した行にジャンプします (最下段の実行フレームにいるときのみ) 。
  デバッガでは、 f_fileno を書き込むことで、ジャンプ命令 (Set Next Statement 命令とも呼ばれます) を実装できます。
"""
import sys

def none(args):
    if args == None:
        return "NONE"
    return args


def myproperty(function):
    print function
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':function.__doc__}
    def probe_func(frame, event, arg):
        print frame
        print " ".join(("event",event)) + " " +  " ".join(("arg",none(arg)))
        if event == 'return':
            print frame.f_locals
            locals = frame.f_locals #@ReservedAssignment
            func_locals.update(dict((k, locals.get(k)) for k in keys))
            sys.settrace(None)
        return probe_func
    sys.settrace(probe_func)
    function()
    print func_locals
    return property(**func_locals)

#====== Example =======================================================

from math import radians, degrees

class Angle(object):
    '''The asngle in radians'''
    def __init__(self, rad):
        self._rad = rad

    @myproperty
    def rad(): #@NoSelf
        '''The angle in radians'''
        def fget(self):
            '''The angle in radians'''
            return self._rad
        def fset(self, angle):
            '''The angle in radians'''
            print angle
            if isinstance(angle, Angle):
                print "yes"
                angle = angle.rad
            self._rad = float(angle)

    @myproperty
    def deg(): #@NoSelf
        '''The angle in degrees'''
        def fget(self):
            '''The angle in degrees'''
            return degrees(self._rad)
        def fset(self, angle):
            '''The angle in degrees'''
            if isinstance(angle, Angle):
                angle = angle.deg
            self._rad = radians(angle)

if __name__ == '__main__':
    a =  Angle(2)
    #print dir(a)
    a.rad = 3
    print a.rad
    print a.deg
    a.deg = 3
    print a.rad

