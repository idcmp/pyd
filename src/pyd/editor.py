'''
Created on Apr 24, 2011

@author: idcmp
'''

import os;
import subprocess

def launch(filename,linenumber):
    print "edit %s on line %d" %( filename,linenumber)
    subprocess.call(["emacs",filename])
