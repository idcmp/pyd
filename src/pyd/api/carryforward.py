'''Part of the API which deals with copying forward data from older weeks into newer weeks.

Generally this is triggered when there's a "new" week.  This
mechanism is responsible for pushing todo entries forward and the timesheet mechanism.

@author: idcmp
'''

import sys

from datetime import date

from api.diaryreader import DiaryReader
from api.diarywriter import DiaryWriter
import api.diarymodel

import api.naming as naming

model = api.diarymodel

def perform_carryforward():
    '''Perform as many carryforwards as needed.

    Walk back through weeks until the week is non-persistent or carryforward is true.  Then perform
    carry-forward on the oldest week without carryforward set.  Repeat until we're carrying forward
    last week until this week.
    '''
    
    offset = 1
    while True:
        weekname = naming.relative_name(offset)
        week = DiaryReader().read_file(weekname)
        if week.has_carryforward() or week.persistent == False:
            break
        offset += 1
    
    if offset == 1:
        # nothing to carry forward
        return False

    offset -= 1
    fromname = naming.relative_name(offset)
    toname = naming.relative_name(offset - 1)

    print "carry from %s to %s" % (fromname,toname)
        
    fromweek = DiaryReader().read_file(fromname)
    toweek = DiaryReader().read_file(toname)
    
    _carryforward(fromweek, toweek)

    DiaryWriter().write_file(fromname, fromweek)
    DiaryWriter().write_file(toname, toweek)

def _carryforward(fromweek, toweek):
    
    co = model.CarryForwardIndicator()
    fromweek.entries.append(co)
    
    fromweek.dump(sys.stdout)
    carryover = find_todos_in_week(fromweek)
    for c in carryover:
        print "xxx"
        c.dump(sys.stdout)
        
    for c in carryover:
        toweek.entries.prepend(c)
    
    ff = model.FreeformWeekEntry("## touched!")
    toweek.entries.append(ff)
    return

def find_todos_in_week(week):
    todos = []
    
    for entry in week.entries:
        if (isinstance(entry, model.DayTodo)): todos.append(entry)
        
    for day in week.days():
        for todo in day.todos():
            todos.append(todo)
            
    for day in week.days():
        for done in day.dones():
            for todo in todos:
                if todo.seq == done.seq:
                    print "remove"
                    print todo.seq
                    todos.remove(todo)
                    break
    return todos
