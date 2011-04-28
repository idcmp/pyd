'''
Created on Apr 25, 2011

@author: idcmp
'''

import sys

import pyd.api.naming as naming
import pyd.tools.toolbox as toolbox

if __name__ == '__main__':
    current_diary = naming.current_name()

    todos = toolbox.find_todos_in_file(current_diary)

    for todo in todos:
        todo.dump(sys.stdout)    
