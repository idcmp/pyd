'''
Created on Apr 24, 2011

@author: idcmp
'''


class Week:
    
    def __init__(self, year):
        self.days = list()
        self.todo_carryover = list()
        self.year = year
        
    def add_day(self, day):
        self.days.append(day)

    def add_carryover(self, todo):
        self.todo_carryover.append(todo)

    def dump(self, to):
        for todo in self.todo_carryover:
            todo.dump(to)
        
        if self.todo_carryover.__len__() > 0:
            to.write("\n")

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

class DayMultiBullet(DayActivity):
    
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("-- " + self.msg)
        to.write("\n--\n")
    
class DayDone(DayActivity):
    
    def __init__(self, seq):
        self.seq = int(seq)
    
    def dump(self, to):
        to.write("- done: #%d" % self.seq)
        to.write("\n")

class DayTodo(DayActivity):
    
    highwatermark = 0
    
    def __init__(self, msg, seq=None):
        
        
        if seq != None:
            self.seq = int(seq)
            DayTodo.highwatermark = max (DayTodo.highwatermark, self.seq)
        else:
            self.seq = None

        self.msg = msg
        
            
    def dump(self, to):
        to.write("todo")

        if self.seq == None:
            DayTodo.highwatermark += 1
            self.seq = DayTodo.highwatermark

        to.write("(#%d)" % self.seq)
        to.write(": " + self.msg)
        to.write("\n")
