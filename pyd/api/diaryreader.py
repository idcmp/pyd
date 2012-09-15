"""
This module is in charge of deserializing a diary file.
"""

import codecs
import string
import os

from pyd.api import diarymodel

class DiaryReader:
    """Read a diary file into a diarymodel.
    """

    def debug(self, msg):
        if os.getenv("DEBUG", "0") != "0":
            print msg

    def __init__(self):
        """Initialize the reading stack. The bottom-most stack frame is a None."""
        self.state_stack = list()
        self.state_stack.append(None)

    def read_file(self, filename):
        """Read in filename, passing each line to _handle_line.  Note: If filename is not
        found, this method will return an empty week whose persistent field is set to false."""

        self.persistent = True
        try:
            # We pass parent=None, line=filename in as the first-ever entry to the handlers,
            # this allows Week to create itself based on the filename.
            self._handle_line(filename)
            with codecs.open(filename, encoding='utf-8') as diary:
                for line in diary:
                    # A raw line is stripped of trailing spaces.
                    cooked = string.rstrip(line)
                    self._handle_line(cooked)
        except IOError:
            self.persistent = False

        # Now the file has been completely read.  We pop the stack
        # until we find the Week node, or until we find None.  This
        # part of the code is the only part that actually knows that
        # Week is the top most parent.
        while True:
            frame = self.state_stack.pop()
            if isinstance(frame, diarymodel.Week):
                frame.persistent = self.persistent
                return frame
            elif frame is None:
                return None

    def _handle_line(self, line):
        """Private.  Determine which handlers can process a line.  Call each one in
        priority order until one doesn't return False."""

        handler_tuples = []

        self.debug("line: %s" % line)

        # Peek at the top of the stack.
        parent = self.state_stack[len(self.state_stack) - 1]

        for handler in diarymodel.diary_reader:
            # For each handler, see if it can handle this line.
            res = handler.responsibility(parent, line)
            self.debug("%s.responsibility(%s,%s) returned %s" % (handler, parent, line, res))
            if res is True:
                handler_tuples += [(100, handler)]
            elif res is False or res == 0 or res is None:
                continue
            else:
                handler_tuples += [(res, handler)]

        # Sort the handlers so highest ranked ones come first.
        sorted_handlers = sorted(handler_tuples, key=lambda handler: handler[0], reverse=True)

        for v, handler in sorted_handlers:
            # Call the handler.  Handler will return what to do with the stack.
            res = handler.handle_line(parent, line)

            if res is False:
                # handler did not process the line, keep trying.
                continue
            elif res is None:
                # handler processed line and the line ended a particular state.
                self.state_stack.pop()
                return
            elif res == parent:
                # handler processed line and state remained the same.
                return
            else:
                # Handler processed state and wants to push a new state ontop of the stack.
                self.state_stack.append(res)
                return

        print "WARNING: NO HANDLER FOR LINE " + line
