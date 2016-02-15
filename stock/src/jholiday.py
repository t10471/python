"""
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
//_/
//_/  CopyRight(C) K.Tsunoda(AddinBox) 2001 All Rights Reserved.
//_/  ( http://www.h3.dion.ne.jp/~sakatsu/index.htm )
//_/
//_/    この祝日判定コードは『Excel:kt関数アドイン』で使用しているものです。
//_/    この関数では、２００７年施行の改正祝日法(昭和の日)までを
//_/  　サポートしています(９月の国民の休日を含む)。
//_/
//_/  (*1)このコードを引用するに当たっては、必ずこのコメントも
//_/      一緒に引用する事とします。
//_/  (*2)他サイト上で本マクロを直接引用する事は、ご遠慮願います。
//_/      【 http://www.h3.dion.ne.jp/~sakatsu/holiday_logic.htm 】
//_/      へのリンクによる紹介で対応して下さい。
//_/  (*3)[ktHolidayName]という関数名そのものは、各自の環境に
//_/      おける命名規則に沿って変更しても構いません。
//_/
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

 追記 SETOGUCHI Mitsuhiro      http://straitmouth.jp/

 * 2007/May/26
 このスクリプトは JavaScript 用判定コード
  http://www.h3.dion.ne.jp/~sakatsu/holiday_logic.htm#JS
 を元に、Python 向けに移植したものです。

 holiday_name() は、年、月、日の3つの整数の引数を取ります。
 不適切な値を与えると、 ValueError が発生します。
 与えた日付が日本において何らかの祝日であれば、その名前が Unicode で返ります。
 祝日でない場合は None が返ります。

"""


import datetime
import math
import argparse

MONDAY, TUESDAY, WEDNESDAY = 0, 1, 2


def _vernal_equinox(y):
    """整数で年を与えると、その年の春分の日が3月の何日であるかを返す
"""
    if y <= 1947:
        d = 0
    elif y <= 1979:
        d = math.floor(20.8357  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2099:
        d = math.floor(20.8431  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2150:
        d = math.floor(21.8510  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    else:
        d = 0

    return d

def _autumn_equinox(y):
    """整数で年を与えると、その年の秋分の日が9月の何日であるかを返す
"""
    if y <= 1947:
        d = 0
    elif y <= 1979:
        d = math.floor(23.2588  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2099:
        d = math.floor(23.2488  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2150:
        d = math.floor(24.2488  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    else:
        d = 0

    return d

def holiday_name(year=None, month=None, day=None, date=None):

    if date is None:
        date = datetime.date(year, month, day)

    if date < datetime.date(1948, 7, 20):
        return None

    funcs = ['_january', '_february', '_march', '_april', '_may', '_june',
             '_july', '_august', '_september', '_october', '_november', '_december']
    name = globals()[funcs[date.month - 1]](date)

    # 振替休日
    if not name and date.weekday() == MONDAY:
        prev = date + datetime.timedelta(days=-1)
        if holiday_name(prev.year, prev.month, prev.day):
            name = '振替休日'

    return name

def _january(date):
    name = None
    if date.day == 1:
        name = '元日'
    if date.year >= 2000:
        if int((date.day - 1) / 7) == 1 and date.weekday() == MONDAY:
            name = '成人の日'
    else:
        if date.day == 15:
            name = '成人の日'
    return name

def _february(date):
    name = None
    if date.day == 11 and date.year >= 1967:
        name = '建国記念の日'
    if (date.year, date.month, date.day) == (1989, 2, 24):
        name = '昭和天皇の大喪の礼'
    return name

def _march(date):
    name = None
    if date.day == _vernal_equinox(date.year):
        name = '春分の日'
    return name

def _april(date):
    name = None
    if date.day == 29:
        if date.year >= 2007:
            name = '昭和の日'
        elif date.year >= 1989:
            name = 'みどりの日'
        else:
            name = '天皇誕生日'
    if (date.year, date.month, date.day) == (1959, 4, 10):
        name = '皇太子明仁親王の結婚の儀'
    return name

def _may(date):
    name = None
    if date.day == 3:
        name = '憲法記念日'
    if date.day == 4:
        if date.year >= 2007:
            name = 'みどりの日'
        elif date.year >= 1986 and date.weekday() != MONDAY:
            name = '国民の休日'
    if date.day == 5:
        name = 'こどもの日'
    if date.day == 6:
        if date.year >= 2007 and date.weekday() in (TUESDAY, WEDNESDAY):
            name = '振替休日'
    return name

def _june(date):
    name = None
    if (date.year, date.month, date.day) == (1993, 6, 9):
        name = '皇太子徳仁親王の結婚の儀'
    return name

def _july(date):
    name = None
    if date.year >= 2003:
        if int((date.day - 1) / 7) == 2 and date.weekday() == MONDAY:
            name = '海の日'
    if date.year >= 1996 and date.day == 20:
        name = '海の日'
    return name

def _august(date):
    name = None
    return name

def _september(date):
    name = None
    autumn_equinox = _autumn_equinox(date.year)
    if date.day == autumn_equinox:
        name = '秋分の日'
    if date.year >= 2003:
        if int((date.day - 1) / 7) == 2 and date.weekday() == MONDAY:
            name = '敬老の日'
        elif date.weekday() == TUESDAY and date.day == autumn_equinox - 1:
            name = '国民の休日'
    if date.year >= 1966 and date.day == 15:
        name = '敬老の日'
    return name

def _october(date):
    name = None
    if date.year >= 2000:
        if int((date.day - 1) / 7) == 1 and date.weekday() == MONDAY:
            name = '体育の日'
    if date.year >= 1966 and date.day == 10:
        name = '体育の日'
    return name

def _november(date):
    name = None
    if date.day == 3:
        name = '文化の日'
    if date.day == 23:
        name = '勤労感謝の日'
    if (date.year, date.month, date.day) == (1990, 11, 12):
        name = '即位礼正殿の儀'
    return name

def _december(date):
    name = None
    if date.day == 23 and date.year >= 1989:
        name = '天皇誕生日'
    return name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('month', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()
    print(holiday_name(args.year, args.month, args.day))
"""
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
//_/ CopyRight(C) K.Tsunoda(AddinBox) 2001 All Rights Reserved.
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
"""
