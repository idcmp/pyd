'''
Created on Apr 25, 2011

@author: idcmp
'''

import sys

from api.naming import current_name
from tools.toolbox import find_todos_in_file

if __name__ == '__main__':
    current_diary = current_name()

    todos = find_todos_in_file(current_diary)

    for todo in todos:
        todo.dump(sys.stdout)    
