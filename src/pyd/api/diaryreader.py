'''
This module is in charge of deserializing a diary file.
'''

from datetime import datetime, date, time
from collections import deque
import codecs
import string

import re #yeah yeah

import diarymodel

class DiaryReader:
    '''Read a diary file into a diarymodel.
    '''
    def __init__(self):
        self.state = 'ROOT'
        self.linereader = { 'ROOT': self.read_root,
                           'DAY': self.read_day,
                           'MULTILINEACTIVITY': self.read_multiline }
    
    def read_file(self, filename):
        
        # A hack to figure out which year to use.
        if string.find(filename, '2010') > -1:
            year = 2010
        elif string.find(filename, '2011') > -1:
            year = 2011
        elif string.find(filename, '2012') > -1:
            year = 2012
        else:
            year = 2011
  
        self.week = diarymodel.Week(year)
        
        try:
            with codecs.open(filename, encoding='utf-8') as diary:
                for line in diary:
                    cooked = string.rstrip(line)
                    if self.linereader.get(self.state)(cooked) == False:
                        print "Lost text: " + cooked
                        
        except IOError:
            pass
        
        return self.week
    
    def read_multiline(self, line):
        '''Private.'''
        if line == "--":
            self.last_activity.msg = string.rstrip(self.last_activity.msg, "\r\n \t")
            self.state = 'DAY'
            return
        
        self.last_activity.msg += "\n" + line


    def read_day(self, line):
        '''Private.'''
        if len(line) == 0:
            self.state = 'ROOT'
            return
        
        if line.startswith("--"):
            self.last_activity = diarymodel.DayMultiBullet(string.strip(line[2:]))
            self.current_day.add_activity(self.last_activity)
            self.state = 'MULTILINEACTIVITY'
            return
        

        m = re.match(r"todo\(#(.*)\): (.*)", line)
        if m:
            self.last_activity = diarymodel.DayTodo(m.group(2), m.group(1))
            self.current_day.add_activity(self.last_activity)
            return
                
        if line.startswith("todo:"):
            self.last_activity = diarymodel.DayTodo(string.strip(line[5:]))
            self.current_day.add_activity(self.last_activity)
            return

        m = re.match(r"- done: #(\d+)(.*)", line)
        if m:
            self.last_activity = diarymodel.DayDone(m.group(1),m.group(2))
            self.current_day.add_activity(self.last_activity)
            return
    
        if line.startswith("-"):
            self.last_activity = diarymodel.DayBullet(string.strip(line[1:]))
            self.current_day.add_activity(self.last_activity)
            return

        return False

    def read_root(self, line):
        '''Private.'''
        m = re.match(r"todo\(#(.*)\): (.*)", line)
        if m:
            todo = diarymodel.DayTodo(m.group(2), m.group(1))
            self.week.entries.append(todo)
            return

        m = re.match(r"\*\* ((Sun|Mon|Tue|Wed|Thu|Fri|Sat)) (\d+)-(\w+)(.*)", line)
        if m:
            dt = datetime.strptime(m.group(4), "%b")
            self.current_day = diarymodel.Day(date(self.week.year, dt.month, int(m.group(3))))
            self.week.entries.append(self.current_day)
            if m.group(5):
                inout = m.group(5)
                inout = string.strip(inout, "(): ")
                inout = deque(re.split("\s+", inout))
                
                while len(inout) > 0:
                    label = inout.popleft()
                    if re.match("i", label):
                        self.current_day.in_at = inout.popleft()
                    if re.match("o", label):
                        self.current_day.out_at = inout.popleft()
            self.state = 'DAY'   
            return
          
        if len(line) > 0:
            self.week.entries.append(diarymodel.FreeformWeekEntry(line))
            return
        else:
            # is swallowing blank lines considered bad?
            # effectively this pushes floating entries into the previous day
            return
        
        return False
