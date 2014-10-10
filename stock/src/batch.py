#*- coding: utf-8 -*-

from jholiday import holiday_name
from datetime import date


SATURDAY, SUNDAY = 6, 7
WEEKEND = [SATURDAY, SUNDAY]
today = date.today()

day = date.weekday()
day_name = holiday_name(date=today)

def do_weekday():
    pass

#土日休日でない場合
if (day_name is not None) and (day not in WEEKEND):
    do_weekday()



