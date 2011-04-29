'''
Created on Apr 28, 2011

@author: idcmp
'''
import unittest

import datetime

from pyd.api import diarymodel
from pyd.api import diaryreader
from pyd.api import diarywriter

class Test(unittest.TestCase):


    def test_emptyday(self):
        """Freshly created Days must be empty."""
        
        day = diarymodel.Day(datetime.date.today())
        
        self.assertEqual(len(day.dones()), 0)
        self.assertEqual(len(day.todos()), 0)
        self.assertEqual(day.in_at, None)
        self.assertEqual(day.out_at, None)
        
    def test_loopback(self):
        """Day with a few activities must write/read properly."""
        day = diarymodel.Day(datetime.date.today())
        day.add_activity(diarymodel.DayBullet('one'))
        day.add_activity(diarymodel.DayBullet('two'))
        day.add_activity(diarymodel.DayBullet('three'))
        day.add_activity(diarymodel.DayMultiBullet('four\nfive\nsix'))
        
        week = diarymodel.Week(2011)
        week.entries.append(day)
        
        diarywriter.DiaryWriter().write_file("sample2.txt", week)        
        week_in = diaryreader.DiaryReader().read_file("sample2.txt")
        
        day_in = week_in.days()[0]
        
        for i, j in zip(day.activities, day_in.activities):
            self.assertEqual(i, j)


    def test_inout_1(self):
        """Test in/out persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.in_at = "9:12"
        day.out_at = "9:13"
        week = diarymodel.Week(2011)
        week.entries.append(day)

        diarywriter.DiaryWriter().write_file("sample2.txt", week)        
        week_in = diaryreader.DiaryReader().read_file("sample2.txt")

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at,day_in.in_at)
        self.assertEqual(day.out_at,day_in.out_at)

    def test_inout_2(self):
        """Test in (without out) persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.in_at = "9:12"
        week = diarymodel.Week(2011)
        week.entries.append(day)

        diarywriter.DiaryWriter().write_file("sample2.txt", week)        
        week_in = diaryreader.DiaryReader().read_file("sample2.txt")

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at,day_in.in_at)
        self.assertEqual(day.out_at,day_in.out_at)

    def test_inout_3(self):
        """Test (without in)/out persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.out_at = "9:13"
        week = diarymodel.Week(2011)
        week.entries.append(day)

        diarywriter.DiaryWriter().write_file("sample2.txt", week)        
        week_in = diaryreader.DiaryReader().read_file("sample2.txt")

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at,day_in.in_at)
        self.assertEqual(day.out_at,day_in.out_at)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_emptyday']
    unittest.main()
