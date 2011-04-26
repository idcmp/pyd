'''
Created on Apr 25, 2011

@author: idcmp
'''

import sys
import unittest2
import pyd.api.diarymodel
import pyd.api.diarywriter

unittest = unittest2
diarymodel = pyd.api.diarymodel
diarywriter = pyd.api.diarywriter

class Test(unittest.TestCase):


    def test_carryforward_detected(self):
        w = diarymodel.Week(2011)
        co = diarymodel.CarryForwardIndicator()
        assert w.has_carryover() == False
        w.entries.append(co)
        assert w.has_carryover() == True


if __name__ == "__main__":
    unittest.main()
