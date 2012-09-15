#!/usr/bin/python
'''
Created on Sep 14, 2012

Find the last Day before Today and print out all the public bullet points (PublicDayBullet).  This
could be yesterday, or it could be months ago.

@author: idcmp
'''
import sys

from pyd.api import naming
from pyd.api import carryforward as cf
from pyd.api.diarymodel import PublicDayBullet, MAXIMUM_HOLIDAY_WEEKS
from pyd.tools import toolbox

from pyd.api import diaryreader

def try_yesterday(days_to_go_back):
    yesterday_diaryname = naming.relative_name(days_ago=days_to_go_back)

    week = diaryreader.DiaryReader().read_file(yesterday_diaryname)

    if yesterday_diaryname == naming.current_name():
        if len(week.days()) == 0 or toolbox.is_today(week.days()[0]):
            return None

        today_idx = -1
        for i in range(1,len(week.days())-1):
            if toolbox.is_today(week.days()[i]):
                today_idx = i
                break;

        return week.days()[today_idx-1]

    size = len(week.days())
    if (size == 0):
        return None

    return week.days()[size-1]

if __name__ == '__main__':
    current_diary = naming.current_name()
    cf.perform_carryforward()
    toolbox.ensure_current_header_exists(current_diary)

    days_to_go_back = 0
    yesterday = None
    while yesterday == None:
        days_to_go_back += 1
        yesterday = try_yesterday(days_to_go_back)
        if days_to_go_back == MAXIMUM_HOLIDAY_WEEKS * 7:
            print "Couldn't find yesterday."
            exit(0)


    public = filter(lambda entry: isinstance(entry,PublicDayBullet),yesterday.entries)

    yesterday.dump_header(sys.stdout)

    for bullet in public:
        bullet.dump(sys.stdout)
