'''
Created on Apr 25, 2011

@author: idcmp
'''

import sys

from api.naming import current_name
from api.diaryreader import DiaryReader

if __name__ == '__main__':
    current_diary = current_name()

    dr = DiaryReader()
    week = dr.read_file(current_diary)
    
    todos = list()
    for day in week.days():
        for todo in day.todos():
            todos.append(todo)
            
    for day in week.days():
        for done in day.dones():
            for todo in todos:
                if todo.seq == done.seq:
                    todos.remove(todo)
                    break
    
    for todo in todos:
        todo.dump(sys.stdout)    