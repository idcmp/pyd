
'''
Used to create names for diary files.
'''

import datetime
import os;

def currentName():

    now =  datetime.date.today()    
    return diaryFile(now)
     
def diaryFile(my_date):
    create_diary_dir()
    week =  my_date.strftime("%U-%Y")
    return os.path.join(os.environ.get("HOME"),"Diary",week+".txt")

def create_diary_dir():
    try:
        os.makedirs(os.path.join(os.environ.get("HOME"),"Diary"))
    except:
        pass
    