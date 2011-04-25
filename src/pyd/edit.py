'''
Created on Apr 23, 2011

Add an entry to the current diary file.

@author: idcmp
'''

import naming
import editor
import dfile

if __name__ == '__main__':
    current_diary = naming.current_name()
    dfile.ensure_current_header_exists(current_diary)
    
    editor.launch(current_diary,55)
    