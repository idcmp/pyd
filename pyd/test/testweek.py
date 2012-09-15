"""
Created on Apr 25, 2011

@author: idcmp
"""

import unittest2 as unittest
import pyd.api.diarymodel as model
import pyd.api.diaryreader as reader
import pyd.api.diarywriter as writer
import pyd.tools.toolbox as toolbox

import datetime

class Test(unittest.TestCase):
    def test_file_does_not_exist(self):
        """read_file should still return a Week if the file is not found, but week will
        have persistent set to false."""

        dr = reader.DiaryReader()
        week = dr.read_file("i do not exist")

        self.assertNotEqual(week, None)
        self.assertEqual(week.persistent, False)

    def test_file_exists(self):
        """Existing weeks must have persistent set to true."""
        week = model.Week(2011)

        dw = writer.DiaryWriter()
        fn = self.genfilename()
        dw.write_file(fn, week)

        week_in = reader.DiaryReader().read_file(fn)
        self.assertEqual(week_in.persistent, True)

    def test_loopback_multi_day(self):
        """ Loopback test of appending multiple days."""
        week = model.Week(2011)
        day1 = model.Day(datetime.date(year=2011, month=1, day=1))
        day2 = model.Day(datetime.date(year=2011, month=1, day=2))
        week.entries.append(day1)
        week.entries.append(day2)

        fn = self.genfilename()
        writer.DiaryWriter().write_file(fn, week)
        week_in = reader.DiaryReader().read_file(fn)

        self.assertEqual(len(week.entries), len(week_in.entries))
        for i, j in zip(week.entries, week_in.entries):
            self.assertEqual(i, j)


    def test_week_days_finds_days(self):
        """week.days finds days correctly."""
        week = model.Week(2011)
        day1 = model.Day(datetime.date(year=2011, month=1, day=1))
        day2 = model.Day(datetime.date(year=2011, month=1, day=2))
        week.entries.append(day1)
        week.entries.append(day2)
        self.assertEqual(len(week.days()), 2)


    def test_carryforward_detected(self):
        """week.has_carryforward detects CarryForwardIndicator."""
        w = model.Week(2011)
        co = model.CarryForwardIndicator()
        assert w.has_carryforward() == False
        w.entries.append(co)
        assert w.has_carryforward() == True

    def test_ensure_header_exists(self):
        """Ensure ensure_header_exists works."""
        week = model.Week(2011)
        self.assertEqual(len(week.entries), 0)

        dw = writer.DiaryWriter()
        fn = self.genfilename()
        dw.write_file(fn, week)
        toolbox.ensure_current_header_exists(fn)

        dr = reader.DiaryReader()
        week2 = dr.read_file(fn)
        self.assertEqual(len(week2.entries), 1)

    def test_todos_in_week(self):
        week = model.Week(2011)
        self.assertEqual(len(model.find_todos_in_week(week)), 0)

        day = model.Day(datetime.date(year=2011, month=11, day=5))
        week.entries.append(day)
        self.assertEqual(len(model.find_todos_in_week(week)), 0)

        todo = model.DayTodo("yup")
        day.entries.append(todo)

        self.assertEqual(len(model.find_todos_in_week(week)), 1)

    def genfilename(self):
        import sys

        return "sample-" + sys._getframe(1).f_code.co_name + ".txt"

if __name__ == "__main__":
    unittest.main()

