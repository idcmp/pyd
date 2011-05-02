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


    def test_multi_line_bullet(self):
        """Test multiline bullet with no text on the -- line."""
        pass

    def test_multi_line_bullet2(self):
        """Test multiline bullet with text on the -- line."""
        pass
    
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
        day.entries.append(diarymodel.DayBullet('one'))
        day.entries.append(diarymodel.DayBullet('two'))
        day.entries.append(diarymodel.DayBullet('three'))
        day.entries.append(diarymodel.DayMultiBullet('four\nfive\nsix'))
        
        week = diarymodel.Week(2011)
        week.entries.append(day)

        fn = self.genfilename()
        diarywriter.DiaryWriter().write_file(fn, week)        
        week_in = diaryreader.DiaryReader().read_file(fn)
        
        day_in = week_in.days()[0]
        
        for i, j in zip(day.entries, day_in.entries):
            self.assertEqual(i, j)


    def test_inout_1(self):
        """Test in/out persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.in_at = "9:12"
        day.out_at = "9:13"
        week = diarymodel.Week(2011)
        week.entries.append(day)

        fn = self.genfilename()
        diarywriter.DiaryWriter().write_file(fn, week)        
        week_in = diaryreader.DiaryReader().read_file(fn)

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at, day_in.in_at)
        self.assertEqual(day.out_at, day_in.out_at)

    def test_inout_2(self):
        """Test in (without out) persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.in_at = "9:12"
        week = diarymodel.Week(2011)
        week.entries.append(day)

        fn = self.genfilename()
        diarywriter.DiaryWriter().write_file(fn, week)        
        week_in = diaryreader.DiaryReader().read_file(fn)

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at, day_in.in_at)
        self.assertEqual(day.out_at, day_in.out_at)

    def test_inout_3(self):
        """Test (without in)/out persistence."""
        day = diarymodel.Day(datetime.date.today())
        day.out_at = "9:13"
        week = diarymodel.Week(2011)
        week.entries.append(day)
        
        fn = self.genfilename()
        diarywriter.DiaryWriter().write_file(fn, week)        
        week_in = diaryreader.DiaryReader().read_file(fn)

        day_in = week_in.days()[0]
        self.assertEqual(day.in_at, day_in.in_at)
        self.assertEqual(day.out_at, day_in.out_at)

    def genfilename(self):
        import sys
        return "sample-" + sys._getframe(1).f_code.co_name + ".txt"

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_emptyday']
    unittest.main()
