'''
Created on Apr 24, 2011

@author: idcmp
'''

import datetime

class Week:
    
    def __init__(self):
        self.days = list()
        self.todo_carryover = list()
        
    def add_day(self, day):
        self.days.append(day)

    def dump(self, to):
        for todo in self.todo_carryover:
            todo.dump(to)
        
        first_day = True
        for day in self.days:
            if first_day == False:
                to.write("\n")
            day.dump(to)
            first_day = False
            
class Day(object):
    
    def add_activity(self, act):
        self.activities.append(act)
        
    def __init__(self, my_day):
        self.my_day = my_day
        self.activities = list()
        self.in_at = None
        self.out_at = None
        
    def set_in_at(self, in_at):
        self.in_at = in_at
    
    def set_out_at(self, out_at):
        self.out_at = out_at

    def dump(self, to):
        to.write("** " + self.my_day.strftime("%a %d-%b"))
        if self.in_at != None or self.out_at != None:
            to.write(" (")

            if self.in_at != None:
                to.write("in " + self.in_at)
                
                if self.out_at != None:
                    to.write(" ")
            
            if self.out_at != None:
                to.write("out " + self.out_at)
            
            to.write(")")

        to.write("\n")
        
        for activity in self.activities:
                activity.dump(to)
        
class DayActivity:
    
    def __init__(self):
        self.msg = None
        
    def dump(self, to):
        pass
        
class DayBullet(DayActivity):
    
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("- " + self.msg)
        to.write("\n")
        pass
    
class DayTodo(DayActivity):
    
    highwatermark = 0
    
    def __init__(self, msg, seq=None):
        self.seq = seq
        self.msg = msg
        DayTodo.highwatermark = max (DayTodo.highwatermark, self.seq)
            
    def dump(self, to):
        to.write("todo")

        if self.seq == None:
            DayTodo.highwatermark += 1
            self.seq = DayTodo.highwatermark

        to.write("(#%d)" % self.seq)
        to.write(": " + self.msg)
        to.write("\n")
