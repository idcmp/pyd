'''
Created on Apr 24, 2011

@author: idcmp
'''

import subprocess
import os

DEFAULT_EDITOR = "emacs"

AT_END = {
    # Emacs variants
    'emacs': ["-nw","+9999"],
    'nano': [ "+9999"],
    'xemacs': ["+9999"],
    # vi(m) variants
    'vi': ["+9999"],
    'vim': ["+9999"],
    # Textmate (Mac users)
    'mate': ["-l", "9999"],
    'mate_wait': ["-l", "9999"]
}

def launch(filename):
    editor = resolve_editor()
    position = at_end_options(editor)
        
    subprocess.call([editor] + position + [filename])

def resolve_editor():
    editor = os.getenv("EDITOR")
    if editor is None:
        return DEFAULT_EDITOR
    return editor

def at_end_options(editor):
    """Returns the appropriate options for positioning the editor at
    the end of the file. This function attempts to parse the random
    weird values people set EDITOR to, including bare commands,
    commands with arguments, and commands with paths.
    """
    # Trim off any trailing command-line arguments
    editor = editor.split()[0]
    
    path, binary = os.path.split(editor)
    return AT_END.get(binary, [])
