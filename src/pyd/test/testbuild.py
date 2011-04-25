'''
Created on Apr 24, 2011

@author: idcmp
'''
import unittest2 as unittest

import sys
import datetime

import pyd.diarymodel as diary

class Test(unittest.TestCase):

    def test_simple(self):
        week = diary.Week()
        for n in [ 24, 25, 26, 27]:
            day = diary.Day(datetime.date(2011, 4, n))
            
            day.set_in_at("9:00")
            day.set_out_at("17:00")
            
            day.add_activity(diary.DayTodo("Don't (before) Forget The Milk"))
            
            for a in range(1, 5):
                day.add_activity(diary.DayBullet("Did thing %d" % a))

            day.add_activity(diary.DayTodo("Don't (after) Forget The Milk"))
                
            
            week.add_day(day)
        
        week.dump(sys.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
