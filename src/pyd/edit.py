'''
Created on Apr 23, 2011

Add an entry to the current diary file.

@author: idcmp
'''

from api.naming import current_name
from api.editor import launch
from tools.dfile import ensure_current_header_exists, read_and_rewrite

from codecs import open

if __name__ == '__main__':
    current_diary = current_name()
    ensure_current_header_exists(current_diary)
    
    with open(current_diary,mode='a',encoding='utf-8') as f:
        f.write("- ")
    
    launch(current_diary)
    read_and_rewrite(current_diary)
