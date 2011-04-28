'''
Created on Apr 23, 2011

Add an entry to the current diary file.

@author: idcmp
'''

import api.naming as naming
import api.editor as editor
import api.carryforward as cf
import tools.toolbox as toolbox

from codecs import open

if __name__ == '__main__':
    current_diary = naming.current_name()
    cf.perform_carryforward()
    toolbox.ensure_current_header_exists(current_diary)
    
    with open(current_diary, mode='a', encoding='utf-8') as f:
        f.write("- ")
    
    editor.launch(current_diary)
    toolbox.read_and_rewrite(current_diary)
