# -*- coding: utf-8 -*-

"""
sys.settrace(tracefunc)(原文)
システムのトレース関数を登録します。トレース関数は Python のソースデバッガを実装するために使用することができます。
トレース関数はスレッド毎に設定することができるので、デバッグを行う全てのスレッドで settrace() を呼び出し、トレース関数を登録してください。
Trace関数は3つの引数: frame, event, arg を受け取る必要があります。 event は文字列です。
 'call', 'line', 'return', 'exception', 'c_call', 'c_return', 'c_exception' のどれかが渡されます。 arg はイベントの種類によって異なります。
trace 関数は (event に 'call' を渡された状態で) 新しいローカルスコープに入るたびに呼ばれます。
この場合、そのスコープで利用するローカルの trace 関数か、そのスコープを trace しないのであれば None を返します。
ローカル trace 関数は自身への参照 (もしくはそのスコープの以降の trace を行う別の関数) を返すべきです。
もしくは、そのスコープの trace を止めるために None を返します。
event には以下の意味があります。
'call'
関数が呼び出された(もしくは、何かのコードブロックに入った)。グローバルの trace 関数が呼ばれる。
 arg は None が渡される。戻り値はローカルの trace 関数。
'line'
インタプリタが新しい行を実行しようとしている。または、ループの条件で最実行しようとしている。
ローカルの trace 関数が呼ばれる。 arg は None 。戻り値は新しいローカルの trace 関数。
これがどのように振る舞うかの詳細な説明は、 Objects/lnotab_notes.txt を参照のこと。
'return'
関数(あるいは別のコードブロック)から戻ろうとしている。ローカルの trace 関数が呼ばれる。
arg は返されようとしている値、または、このイベントが例外が送出されることによって起こったなら None 。 trace 関数の戻り値は無視される。
'exception'
例外が発生した。ローカルの trace 関数が呼ばれる。
arg は (exception, value, traceback) のタプル。戻り値は新しいローカルの trace 関数。
'c_call'
C 関数(拡張関数かビルトイン関数)が呼ばれようとしている。 arg は C 関数オブジェクト。
'c_return'
C 関数から戻った。 arg は C の関数オブジェクト。
'c_exception'
C 関数が例外を発生させた。 arg は C の関数オブジェクト。
例外が呼び出しチェインを辿って伝播していくことに注意してください。 'exception' イベントは各レベルで発生します。

code と frame オブジェクトについては、 標準型の階層 を参照してください。

コードオブジェクト
コードオブジェクトは バイトコンパイルされた (byte-compiled) 実行可能な Python コード、別名バイトコード(bytecode) を表現します。
コードオブジェクトと関数オブジェクトの違いは、
関数オブジェクトが関数のグローバル変数 (関数を定義しているモジュールのグローバル) に対して明示的な参照を持っているのに対し、
コードオブジェクトにはコンテキストがないということです;
また、関数オブジェクトではデフォルト引数値を記憶できますが、
コードオブジェクトではできません (実行時に計算される値を表現するため)。
関数オブジェクトと違い、コードオブジェクトは変更不可能で、変更可能なオブジェクトへの参照を (直接、間接に関わらず) 含みません。

読み出し専用の特殊属性:
co_name は関数名を表します;
co_argcount は固定引数 (positional argument) の数です;
co_nlocals は関数が使う (引数を含めた) ローカル変数の数です;
co_varnames はローカル変数名の入ったタプルです (引数名から始まっています);
co_cellvars はネストされた関数で参照されているローカル変数の名前が入ったタプルです;
co_freevars は自由変数の名前が入ったタプルです。 co_code はバイトコード列を表現している文字列です;
co_consts はバイトコードで使われているリテラルの入ったタプルです;
co_names はバイトコードで使われている名前の入ったタプルです;
co_filename はバイトコードのコンパイルが行われたファイル名です;
co_firstlineno は関数の最初の行番号です;
co_lnotab はバイトコードオフセットから行番号への対応付けをコード化した文字列です (詳細についてはインタプリタのソースコードを参照してください);
co_stacksize は関数で (ローカル変数の分も含めて) 必要なスタックサイズです;
co_flags はインタプリタ用の様々なフラグをコード化した整数です。

以下のフラグビットが co_flags で定義されています:
0x04 ビットは、関数が *arguments 構文を使って任意の数の固定引数を受理できる場合に立てられます;
0x08 ビットは、関数が **keywords 構文を使ってキーワード引数を受理できる場合に立てられます;
0x20 ビットは、関数がジェネレータである場合に立てられます。

将来機能 (future feature) 宣言 (from __future__ import division) もまた、
 co_flags のビットを立てることで、コードオブジェクトが特定の機能を有効にしてコンパイルされていることを示します:
 0x2000 ビットは、関数が将来機能を有効にしてコンパイルされている場合に立てられます;
 以前のバージョンの Python では、 0x10 および 0x1000 ビットが使われていました。

co_flags のその他のビットは将来に内部的に利用するために予約されています。

コードオブジェクトが関数を表現している場合、 co_consts の最初の要素は関数のドキュメンテーション文字列になります。
ドキュメンテーション文字列が定義されていない場合には None になります。

linecache モジュールは、キャッシュ (一つのファイルから何行も読んでおくのが一般的です) を使って、内部で最適化を図りつつ、
任意のファイルの任意の行を取得するのを可能にします。
traceback モジュールは、整形されたトレースバックにソースコードを含めるためにこのモジュールを利用しています。


linecache.getline(filename, lineno[, module_globals])(原文)
filename という名前のファイルから lineno 行目を取得します。
この関数は決して例外を発生させません — エラーの際には '' を返します。 (行末の改行文字は、見つかった行に含まれます。)
filename という名前のファイルが見つからなかった場合、
モジュールの、つまり、 sys.path でそのファイルを探します。
zipfileやその他のファイルシステムでないimport元に対応するためまず
modules_globals の PEP 302 __loader__ をチェックし、そのあと sys.path を探索します。

バージョン 2.5 で追加: パラメータ module_globals の追加.
"""
import sys
import os
import linecache

def trace(f):
    def globaltrace(frame, why, arg):
        if why == "call":
            return localtrace
        return None

    def localtrace(frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno

            bname = os.path.basename(filename)
            print "%s(%d): %s" % (bname, lineno,
                                  linecache.getline(filename, lineno)),
        return localtrace

    def _f(*args, **kwds):
        sys.settrace(globaltrace)
        result = f(*args, **kwds)
        sys.settrace(None)
        return result

    return _f

@trace
def inc(i):
    if i < 5:
        i += 1
    else:
        i += 6
    for i in range(i):
        print i
    return i + 1

print inc(2)
print inc(6)