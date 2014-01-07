"""
A model to describe a week in the life of pyd.

Model types must implement:
    - dump(self,stream) which serializes
    - responsibility(self,parent,line) : see WeekEntry.responsibility
    - handle_line(self,parent,line) : see WeekEntry.handle_line
    - self.parent - returns the parent of the current object.
    - self.entries - if the class pushes itself as parent during handle_line, it must support
    adding children through self.entries.append()
"""

import string
import re
from datetime import datetime, date
from collections import deque

# When seeking backwards for something, stop looking after this many weeks.
MAXIMUM_HOLIDAY_WEEKS = 13

diary_reader = []
week_entries = []
day_activities = []
carryforward_participants = []

def carryforward(cls):
    carryforward_participants.append(cls)
    diary_reader.append(cls)
    return cls


def weekentry(cls):
    week_entries.append(cls)
    diary_reader.append(cls)
    return cls


def dayactivity(cls):
    day_activities.append(cls)
    diary_reader.append(cls)
    return cls


def linehandler(cls):
    diary_reader.append(cls)
    return cls


@linehandler
class Week:
    def __init__(self, year):
        self.entries = []
        self.year = year
        self.persistent = False

    def has_carryforward(self):
        return len(filter(lambda entry: isinstance(entry, CarryForwardIndicator), self.entries)) != 0

    def days(self):
        return filter(lambda entry: isinstance(entry, Day), self.entries)

    def dump(self, to):
        for entry in self.entries:
            entry.dump(to)

    @classmethod
    def responsibility(cls, parent, line):
        return  (parent is None) or  (isinstance(parent, Week) and (line == "" or line is None))

    @classmethod
    def handle_line(cls, parent, line):
        if line is None:
            return None

        if isinstance(parent, Week) and line == "":
            return parent

        # A hack to figure out which year to use.
        if string.find(line, '2010') > -1:
            year = 2010
        elif string.find(line, '2011') > -1:
            year = 2011
        elif string.find(line, '2012') > -1:
            year = 2012
        elif string.find(line, '2013') > -1:
            year = 2013
        elif string.find(line, '2014') > -1:
            year = 2014
        elif string.find(line, '2015') > -1:
            year = 2015
        elif string.find(line, '2016') > -1:
            year = 2016
        elif string.find(line, '2017') > -1:
            year = 2017
        else:
            year = 2011

        week = Week(year)
        week.parent = parent
        return week


class WeekEntry(object):
    """Abstract class from which all things in a week are derived.
    
        Usually a week just has Day objects in it, however directly referencing Day runs into a challenge
        where there may be other kinds of entries (such as freeform text) that we don't want to lose.
    """

    def dump(self, to):
        pass

    @classmethod
    def responsibility(cls, parent, line):
        """Return True, False, None or an integer depending on if this class is responsible for
        parsing a given line.  False, None and 0 are identical (not responsible).  True is the same
        as returning an integer of 100.  If multiple classes return integers or true, the one with
        the highest value is called first to handle the line.  
        
        Results are effectively undefined for multiple classes returning the same value.  
        Note that a call with parent of None and line equaling the filename as arguments is always done first to find the parent node.
        Note that a call with the current parent and a line equaling None is done to indicate EOF."""
        return False

    @classmethod
    def handle_line(cls, parent, line):
        """When this handler is elected, this method will be called. Implementors must 1) attach
        newly created entities to the parent correctly, 2) return the appropriate "parent" to push
        onto the stack (or False). Returning the same parent as was passed in keeps the parent the same. Returning
        None will pop another layer off the stack.  Returning False will indicate that the particular
        handler was unable to process the lineNote: The last entry in the stack is None"""
        return False


@weekentry
class FreeformWeekEntry(WeekEntry):
    """Generic place holder for "things we found in the file that aren't something else."""

    def __init__(self, text):
        self.text = text

    def dump(self, to):
        to.write(self.text + "\n")

    @classmethod
    def responsibility(cls, parent, line):
        """Defacto handler for otherwise unhandled lines who have Week as their parent."""
        if isinstance(parent, Week):
            return 1
        return False

    @classmethod
    def handle_line(cls, parent, line):
        ff = FreeformWeekEntry(line)
        parent.entries.append(ff)
        ff.parent = parent
        return parent


@weekentry
class CarryForwardIndicator(WeekEntry):
    indicator = "++carriedforward"

    @classmethod
    def responsibility(cls, parent, line):
        return line == CarryForwardIndicator.indicator

    @classmethod
    def handle_line(cls, parent, line):
        cf = CarryForwardIndicator()
        cfp = parent

        if isinstance(cfp, Day):
            cfp = cfp.parent

        cf.parent = cfp
        cfp.entries.append(cf)
        return parent

    def dump(self, to):
        to.write(CarryForwardIndicator.indicator + "\n")


@weekentry
class Day(WeekEntry):
    """A day contains DayActivities and some metadata.
    
    A day knows which year its in from the Week.
    """

    activity_types = []

    def todos(self):
        return filter(lambda entry: isinstance(entry, DayTodo), self.entries)

    def dones(self):
        return filter(lambda entry: isinstance(entry, DayDone), self.entries)

    def __init__(self, my_day):
        self.my_day = my_day
        self.entries = []
        self.in_at = None
        self.out_at = None

    def set_in_at(self, in_at):
        self.in_at = in_at

    def set_out_at(self, out_at):
        self.out_at = out_at

    def dump_header(self, to):
        to.write("\n** " + self.my_day.strftime("%a %d-%b"))

        # It's perfectly valid to have no "out", in which case a closing paren is
        # not supposed to be there.
        if self.in_at is not None or self.out_at is not None:
            to.write(" (")

            if self.in_at is not None:
                to.write("in " + self.in_at)
                if self.out_at is not None:
                    to.write(" ")

            if self.out_at is not None:
                to.write("out " + self.out_at)
                to.write(")")

        to.write("\n")

    def dump(self, to):
        self.dump_header(to)

        for entry in self.entries:
            entry.dump(to)

    @classmethod
    def responsibility(cls, parent, line):
        if line.startswith("** ") and isinstance(parent, Week):
            return True
        elif line == "" and isinstance(parent, Day):
            return True


    @classmethod
    def handle_line(cls, parent, line):
        if line == "":
            # Pop stack out of Day.
            return None

        m = re.match(r"\*\* ((Sun|Mon|Tue|Wed|Thu|Fri|Sat)) (\d+)-(\w+)(.*)", line)
        if m:
            dt = datetime.strptime(m.group(4), "%b")
            current_day = Day(date(parent.year, dt.month, int(m.group(3))))
            current_day.parent = parent
            parent.entries.append(current_day)
            if m.group(5):
                inout = m.group(5)
                inout = string.strip(inout, "(): ")
                inout = deque(re.split("\s+", inout))

                while len(inout) > 0:
                    label = inout.popleft()
                    if re.match("i", label):
                        current_day.in_at = inout.popleft()
                    if re.match("o", label):
                        current_day.out_at = inout.popleft()

            return current_day
        return False

    def __eq__(self, other):
        """Two Day objects are identical if they have the same day/month.
        
        It's not safe to compare Day objects from different years.
        """
        if not isinstance(other, Day):
            return False

        return other.my_day.month == self.my_day.month and other.my_day.day == self.my_day.day

    def __ne__(self, other):
        return not self.__eq__(other)


class DayActivity:
    """Abstract class for activities that occur in a day."""

    public = False

    def __init__(self):
        self.msg = None

    def dump(self, to):
        pass

    @classmethod
    def responsibility(cls, parent, line):
        return False

    @classmethod
    def handle_line(cls, parent, line):
        return parent

    def __ne__(self, other):
        return not self.__eq__(other)


@dayactivity
class FreeformDayEntry(DayActivity):
    """Generic place holder for things we found in the file that aren't something else, but for Days."""

    def __init__(self, text):
        DayActivity.__init__(self)
        self.text = text

    def dump(self, to):
        to.write(self.text + "\n")

    @classmethod
    def responsibility(cls, parent, line):
        """Defacto handler for otherwise unhandled lines who have Day as their parent."""
        if isinstance(parent, Day):
            return 1
        return False

    @classmethod
    def handle_line(cls, parent, line):
        ff = FreeformDayEntry(line)
        parent.entries.append(ff)
        ff.parent = parent
        return parent


@dayactivity
class DayBullet(DayActivity):
    """A thing you did today.  Starts with "- " and contains a single line of text.
    """

    def __init__(self, msg, public=False):
        DayActivity.__init__(self)
        self.msg = msg
        self.public = public

    def dump(self, to):
        if self.public:
            to.write("+ ")
        else:
            to.write("- ")

        to.write(self.msg)
        to.write("\n")

    @classmethod
    def responsibility(cls, parent, line):
        if (line.startswith("- ") or line.startswith("+ ")) and isinstance(parent, Day):
            return 20
        elif line == "-" and isinstance(parent, Day):
            return 50

    @classmethod
    def handle_line(cls, parent, line):
        if line == "-" or line == "+":
            return parent

        bullet = DayBullet(string.strip(line[1:]))
        bullet.parent = parent
        parent.entries.append(bullet)

        if line[0] == "+":
            bullet.public = True
        else:
            bullet.public = False

        return parent

    def __eq__(self, other):
        return isinstance(other, DayBullet) and other.msg == self.msg


@dayactivity
class DayMultiBullet(DayActivity):
    """A thing you did today; supporting multiple lines.  
    
    Starts with "--" (followed optionally by text) and ends with "--" on a line by itself.
    """

    def __init__(self, msg):
        DayActivity.__init__(self)
        self.msg = msg

    def dump(self, to):
        to.write("-- " + self.msg)
        to.write("\n--\n")

    @classmethod
    def responsibility(cls, parent, line):
        """This class will push itself onto the stack."""
        return (line.startswith("--") and isinstance(parent, Day)) or isinstance(parent, DayMultiBullet)

    @classmethod
    def handle_line(cls, parent, line):
        """If we're already reading a multibullet, then continue until we reach "--" on a blank line.
        Otherwise, create a new DayMultiBullet and push it onto the stack."""

        if isinstance(parent, DayMultiBullet):
            if line == "--":
                parent.msg = string.rstrip(parent.msg, "\r\n \t")
                return
            parent.msg += "\n" + line
            return parent
        else:
            last_activity = DayMultiBullet(string.strip(line[2:]))
            last_activity.parent = parent
            parent.entries.append(last_activity)
            return last_activity

    def __eq__(self, other):
        return isinstance(other, DayMultiBullet) and other.msg == self.msg


@dayactivity
class DayDone(DayActivity):
    """Mark a TODO as done.  Format is "- done: #NN" where NN is the todo number.
    """

    def __init__(self, seq, msg=None):
        DayActivity.__init__(self)
        self.seq = int(seq)
        self.msg = msg

    def dump(self, to):
        to.write("- done: #%d" % self.seq)
        if self.msg:
            to.write(self.msg)
        to.write("\n")

    @classmethod
    def responsibility(cls, parent, line):
        return line.startswith("- done:") and isinstance(parent, Day)

    @classmethod
    def handle_line(cls, parent, line):
        m = re.match(r"- done: #(\d+)(.*)", line)
        if m:
            last_activity = DayDone(m.group(1), m.group(2))
            last_activity.parent = parent
            parent.entries.append(last_activity)
            return parent
        return False

    def __eq__(self, other):
        return isinstance(other, DayDone) and self.seq == other.seq and other.msg == self.msg


@carryforward
@dayactivity
class DayTodo(DayActivity):
    """Todo list management.
    
    This class breathes some life into pyd.  Entries starting with "todo:" can be added and
    pyd will automatically rewrite them to include a point-in-time-unique number.  Note that
    the number does not monotonically increase, but simply finds the highest todo # in the current
    week and adds one.
    
    Todo entries not completed at the end of the week are carried over to the next week.
    """

    highwatermark = 0

    def __init__(self, msg, seq=None):
        DayActivity.__init__(self)
        if seq is not None:
            self.seq = int(seq)
            DayTodo.highwatermark = max(DayTodo.highwatermark, self.seq)
        else:
            self.seq = None
        self.msg = msg

    def __eq__(self, other):
        return isinstance(other, DayTodo) and self.seq == other.seq and other.msg == self.msg

    @classmethod
    def carryforward(cls, fromweek, toweek):
        carryover = find_todos_in_week(fromweek)

        for c in carryover:
            toweek.entries.insert(0, c)

    def dump(self, to):
        to.write("- todo")

        if self.seq is None:
            DayTodo.highwatermark += 1
            self.seq = DayTodo.highwatermark

        to.write("(#%d)" % self.seq)
        to.write(": " + self.msg)
        to.write("\n")

    @classmethod
    def responsibility(cls, parent, line):
        return line.startswith("- todo") and (isinstance(parent, Day) or isinstance(parent, Week))

    @classmethod
    def handle_line(cls, parent, line):
        m = re.match(r"- todo\(#(.*)\): (.*)", line)
        if m:
            last_activity = DayTodo(m.group(2), m.group(1))
            last_activity.parent = parent
            parent.entries.append(last_activity)
            return parent

        if line.startswith("- todo:"):
            last_activity = DayTodo(string.strip(line[7:]))
            last_activity.parent = parent
            parent.entries.append(last_activity)
            return parent

        return False


###
# Static helper methods.
###
def find_todos_in_week(week):
    """Return all DayTodo instances in a Week.

    Note this method will return both carryover and daily todo entries in the list, in the order they're found in the Week.
    """

    todos = []

    for entry in week.entries:
        if isinstance(entry, DayTodo): todos.append(entry)

    for day in week.days():
        for todo in day.todos():
            todos.append(todo)

    for day in week.days():
        for done in day.dones():
            for todo in todos:
                if todo.seq == done.seq:
                    todos.remove(todo)
                    break
    return todos

