'''
    SDK ontop of the API
'''

from datetime import date

from pyd.api import diaryreader as reader
from pyd.api import diarywriter as writer
from pyd.api import diarymodel as model
    
def find_todos_in_file(filename):
    dr = reader.DiaryReader()
    week = dr.read_file(filename)
    return model.find_todos_in_week(week)

def ensure_current_header_exists(filename):
    """Ensures the day header for the current day exists in filename.
    
    This will read/rewrite the file to add one.
    """
    
    week = reader.DiaryReader().read_file(filename)
    
    # if we have more than one for whatever reason, that's fine.
    if len(filter(lambda day: day.my_day == date.today(), week.days())) == 0:
        day = model.Day(date.today())
        week.entries.append(day)
        
        writer.DiaryWriter().write_file(filename, week)

def read_and_rewrite(filename):
    """Converts a diary file to a model and back again.
    
    Used after a manual edit to the file occurs to perform any needed synchronization.
    """
    week = reader.DiaryReader().read_file(filename)
    writer.DiaryWriter().write_file(filename, week)

def is_today(day):
    """Is the passed in Day object "today" ?"""
    return model.Day(date.today()) == day
