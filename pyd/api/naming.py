'''
Used to create file names for diary files.
'''

from datetime import datetime, date, timedelta
import os;

def current_name():
    now = date.today()    
    return generate_filename(now)

def relative_name(weeks_ago):
    now = datetime.now()
    then = now - timedelta(weeks=weeks_ago)
    return generate_filename(then)
    
def generate_filename(my_date):
    _create_diary_dir()
    week = my_date.strftime("%U-%Y")
    return os.path.join(os.environ.get("HOME"), "Diary", week + ".txt")

def _create_diary_dir():
    try:
        os.makedirs(os.path.join(os.environ.get("HOME"), "Diary"))
    except:
        pass
    
