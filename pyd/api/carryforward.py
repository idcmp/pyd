'''Part of the API which deals with copying forward data from older weeks into newer weeks.

Generally this is triggered when there's a "new" week. 

This mechanism is responsible for dispatching to DayTodo to push todo
entries forward and the timesheet mechanism.  It calls out to the static method
carryforward on classes decorated with @carryforward.

'''

from pyd.api import diaryreader as reader
from pyd.api import diarywriter as writer
from pyd.api import diarymodel as model
from pyd.api import naming as naming
from pyd.api.diarymodel import MAXIMUM_HOLIDAY_WEEKS

def perform_carryforward():
    '''Perform as many carryforwards as needed.

    Walk back through weeks until the week is non-persistent or carryforward is true.  Then perform
    carry-forward on the oldest week without carryforward set.  Repeat until we're carrying forward
    last week until this week.
    '''
    
    offset = 1
    nonpersistentweeks = 0
    while True:
        weekname = naming.relative_name(offset)
        week = reader.DiaryReader().read_file(weekname)
        if week.persistent == False:
            nonpersistentweeks += 1
        if week.has_carryforward() or nonpersistentweeks == MAXIMUM_HOLIDAY_WEEKS:
            break
        offset += 1
    
    while offset > 1:
        offset -= 1
        fromname = naming.relative_name(offset)
        toname = naming.relative_name(offset - 1)

        fromweek = reader.DiaryReader().read_file(fromname)
        toweek = reader.DiaryReader().read_file(toname)
        
        _carryforward(fromweek, toweek)
    
        writer.DiaryWriter().write_file(fromname, fromweek)
        writer.DiaryWriter().write_file(toname, toweek)
        
    return

def _carryforward(fromweek, toweek):
    """Add the CarryForwardIndicator to the source week and call carryforward on all
    classes annotated with @carryforward."""

    fromweek.entries.append(model.CarryForwardIndicator())
    
    for entry in model.carryforward_participants:
        entry.carryforward(fromweek, toweek)  
    
    return

