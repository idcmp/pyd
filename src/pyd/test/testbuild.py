'''
Created on Apr 24, 2011

@author: idcmp
'''

import unittest2 as unittest

import datetime
import sys

import pyd.diarymodel as diary
import pyd.diaryreader as reader

class Test(unittest.TestCase):


    def test_read(self):
        #reader.read_file(naming.current_name())
        r = reader.DiaryReader()
        
        week = r.read_file("sample.txt")
        
        week.dump(sys.stdout)

    def skip_test_write(self):
        week = diary.Week(2011)
        for n in [ 24, 25, 26, 27]:
            day = diary.Day(datetime.date(week.year, 4, n))
            
            if n == 25 or n == 27:
                day.set_in_at("9:00")

            if n == 26 or n == 27:
                day.set_out_at("17:00")
            
            day.add_activity(diary.DayTodo("Don't (before) Forget The Milk"))
            
            for a in range(1, 5):
                day.add_activity(diary.DayBullet("Did thing %d" % a))

            day.add_activity(diary.DayTodo("Don't (after) Forget The Milk"))
            
            week.add_day(day)
        
        week.dump(sys.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
