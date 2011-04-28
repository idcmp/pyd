'''
Created on Apr 25, 2011

@author: idcmp
'''

import unittest2 as unittest
import pyd.api.diarymodel as model
import pyd.api.diaryreader as reader
import pyd.api.diarywriter as writer
import pyd.tools.toolbox as toolbox

import datetime

class Test(unittest.TestCase):

    def test_carryforward_detected(self):
        w = model.Week(2011)
        co = model.CarryForwardIndicator()
        assert w.has_carryforward() == False
        w.entries.append(co)
        assert w.has_carryforward() == True

    def test_ensure_header_exists(self):
        week = model.Week(2011)
        self.assertEqual(len(week.entries), 0)

        dw = writer.DiaryWriter()
        dw.write_file("sample2.txt", week)
        toolbox.ensure_current_header_exists("sample2.txt")
        
        dr = reader.DiaryReader()
        week2 = dr.read_file("sample2.txt")
        self.assertEqual(len(week2.entries), 1)
        
    def test_todos_in_week(self):
        week = model.Week(2011)
        self.assertEqual(len(model.find_todos_in_week(week)), 0)

        day = model.Day(datetime.date(year=2011, month=11, day=5))
        week.entries.append(day)
        self.assertEqual(len(model.find_todos_in_week(week)), 0)

        todo = model.DayTodo("yup")
        day.activities.append(todo)
        
        self.assertEqual(len(model.find_todos_in_week(week)), 1)


if __name__ == "__main__":
    unittest.main()
