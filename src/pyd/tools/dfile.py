'''

'''

from datetime import date
from api.diaryreader import DiaryReader
from api.diarywriter import DiaryWriter

from api.diarymodel import Day

def ensure_current_header_exists(filename):
    """Ensures the day header for the current day exists in filename.
    
    This will read/rewrite the file to add one.
    """
    
    dr = DiaryReader()
    week = dr.read_file(filename)
    
    def is_today(day): return day.my_day == date.today()
    
    # if we have more than one for whatever reason, that's fine.
    if len(filter(is_today, week.days())) == 0:
        day = Day(date.today())
        week.entries.append(day)
        
        dw = DiaryWriter()
        dw.write_file(filename, week)

def read_and_rewrite(filename):
    """Converts a diary file to a model and back again.
    
    Used after a manual edit to the file occurs to perform any needed synchronization.
    """
    dr = DiaryReader()
    dw = DiaryWriter()
    week = dr.read_file(filename)
    dw.write_file(filename, week)
