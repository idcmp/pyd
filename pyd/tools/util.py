"""
Created on Apr 24, 2011

@author: idcmp
"""

'''
http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python/1695250#1695250
'''

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
