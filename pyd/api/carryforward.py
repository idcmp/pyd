'''Part of the API which deals with copying forward data from older weeks into newer weeks.

Generally this is triggered when there's a "new" week.  This
mechanism is responsible for pushing todo entries forward and the timesheet mechanism.

@author: idcmp
'''

from pyd.api import diaryreader as reader
from pyd.api import diarywriter as writer
from pyd.api import diarymodel as model
from pyd.api import naming as naming

def perform_carryforward():
    '''Perform as many carryforwards as needed.

    Walk back through weeks until the week is non-persistent or carryforward is true.  Then perform
    carry-forward on the oldest week without carryforward set.  Repeat until we're carrying forward
    last week until this week.
    '''
    
    offset = 1
    while True:
        weekname = naming.relative_name(offset)
        week = reader.DiaryReader().read_file(weekname)
        if week.has_carryforward() or week.persistent == False:
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

    co = model.CarryForwardIndicator()
    fromweek.entries.append(co)
    
    for e in model.carryforward_participants:
        e.carryforward(fromweek, toweek)  
    
    return

