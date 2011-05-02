'''
Created on May 1, 2011

@author: idcmp
'''
import unittest2 as unittest


class Test(unittest.TestCase):

    def test_week_scoped_todos(self):
        """Test that todos outside of a Day are found."""
        pass

    def test_day_scoped_todos(self):
        """Test todos in a Day are found."""
        pass
    
    def test_done_todos(self):
        """Test that todos marked done are not found."""

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_week_scoped_todos']
    unittest.main()
