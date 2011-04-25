'''
Created on Apr 24, 2011

@author: idcmp
'''

import subprocess

def launch(filename):
    subprocess.call(["emacs","+9999",filename])
