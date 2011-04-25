'''
Created on Apr 25, 2011

@author: idcmp
'''

import os
from codecs import open

class DiaryWriter:
    
    def write_file(self, filename, week):
        if os.path.isfile(filename):
            os.rename(filename, filename + ".bak")
            
        with open(filename, mode='w', encoding='utf-8') as diaryfile:
            week.dump(diaryfile)
    
