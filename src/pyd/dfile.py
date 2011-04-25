'''

'''

from datetime import datetime, date
import diaryreader
import diarywriter

import diarymodel

def ensure_current_header_exists(filename):

    dr = diaryreader.DiaryReader()
    week = dr.read_file(filename)
    
    def is_today(day): return day.my_day == date.today()
    
    if len(filter(is_today, week.days)) == 0:
        day = diarymodel.Day(date.today())
        week.add_day(day)
        
        writer = diarywriter.DiaryWriter()
        writer.write_file(filename, week)
