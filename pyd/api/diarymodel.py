'''
A model to describe a week in the life of pyd.

Each model class implements dump().

'''

import string

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
            
    @staticmethod
    def responsibility(parent, line):
        if parent is None:
            return True
    
    @staticmethod
    def handle_line(parent, line):
            # A hack to figure out which year to use.
        if string.find(line, '2010') > -1:
            year = 2010
        elif string.find(line, '2011') > -1:
            year = 2011
        elif string.find(line, '2012') > -1:
            year = 2012
        else:
            year = 2011

        return Week(year)
        
class WeekEntry(object):
    """Abstract class from which all things in a week are derived.
    
        Usually a week just has Day objects in it, however directly referencing Day runs into a challenge
        where there may be other kinds of entries (such as freeform text) that we don't want to lose.
    """
    def dump(self, to):
        pass

    @staticmethod
    def responsibility(parent, line):
        """Return True, False, None or an integer depending on if this class is responsible for
        parsing a given line.  False, None and 0 are identical (not responsible).  True is the same
        as returning an integer of 100.  If multiple classes return integers or true, the one with
        the highest value is called to parse the line.  Results are effectively undefined for multiple
        classes returning the same value (but only one will be called).  Note that a call with parent of None
        and line equaling the filename as arguments is always done first to find the parent node."""
        return False
    
    @staticmethod
    def handle_line(parent, line):
        """If this handler is elected, this method will be called. Implementors must 1) attach
        newly created entities to the parent correctly, 2) return the appropriate "parent".  If
        this handler is expecting more data, it can return itself, otherwise it likely wants
        to return the parent it was passed in.  Returning None is the same as returning the passed
        in parent."""
        pass
        
@weekentry
class FreeformWeekEntry(WeekEntry):
    """Generic place holder for "things we found in the file that aren't something else."""
    
    def __init__(self, text):
        self.text = text
        
    def dump(self, to):
        to.write(self.text + "\n")
        
    @staticmethod
    def responsibility(parent, line):
        """Defacto handler for otherwise unhandled lines who have Week as their parent."""
        if isinstance(parent, Week):
            return 1

    @staticmethod
    def handle_line(parent, line):
        ff = FreeformWeekEntry(line)
        parent.entries.append(ff)
        return parent

@weekentry
class CarryForwardIndicator(WeekEntry):

    indicator = "++carriedforward"
    
    @staticmethod
    def responsibility(parent, line):
        return line == CarryForwardIndicator.indicator and isinstance(parent, Week)
    
    @staticmethod
    def handle_line(parent, line):
        cf = CarryForwardIndicator()
        parent.entries.append(cf)
        return parent

    def dump(self, to):
        to.write(CarryForwardIndicator.indicator)
        
@weekentry
class Day(WeekEntry):
    """A day contains DayActivities and some metadata.
    
    A day knows which year its in from the Week.
    """
    
    activity_types = []
    
    def add_activity(self, act):
        self.activities.append(act)

    def todos(self):
        return filter(lambda entry: isinstance(entry, DayTodo), self.activities)
    
    def dones(self):
        return filter(lambda entry: isinstance(entry, DayDone), self.activities)

    def __init__(self, my_day):
        self.my_day = my_day
        self.activities = []
        self.in_at = None
        self.out_at = None
        
    def set_in_at(self, in_at):
        self.in_at = in_at
    
    def set_out_at(self, out_at):
        self.out_at = out_at

    def dump(self, to):
        to.write("\n** " + self.my_day.strftime("%a %d-%b"))
        
        # It's perfectly valid to have no "out", in which case a closing paren is
        # not supposed to be there.
        if self.in_at != None or self.out_at != None:
            to.write(" (")

            if self.in_at != None:
                to.write("in " + self.in_at)
                if self.out_at != None:
                    to.write(" ")

            if self.out_at != None:
                to.write("out " + self.out_at)
                to.write(")")

        to.write("\n")

        for activity in self.activities:
                activity.dump(to)
    
    @staticmethod
    def responsibility(parent, line):
        return line.startswith("** ")
    
    def __eq__(self, other):
        """Two Day objects are identical if they have the same day/month.
        
        It's not safe to compare Day objects from different years.
        """
        return other.my_day.month == self.my_day.month and other.my_day.day == self.my_day.day

    def __ne__(self, other):
        return not self.__eq__(other)
    
class DayActivity:
    """Abstract class for activities that occur in a day."""    

    def __init__(self):
        self.msg = None
        
    def dump(self, to):
        pass

    @staticmethod
    def responsibility(parent, line):
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

@dayactivity
class DayBullet(DayActivity):
    """A thing you did today.  Starts with "- " and contains a single line of text.
    """
            
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("- " + self.msg)
        to.write("\n")

    @staticmethod
    def responsibility(parent, line):
        if line.startswith("- "):
            return 20

    def __eq__(self, other):
        return isinstance(other, DayBullet) and other.msg == self.msg

@dayactivity
class DayMultiBullet(DayActivity):
    """A thing you did today; supporting multiple lines.  
    
    Starts with "--" (followed optionally by text) and ends with "--" on a line by itself.
    """
    
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("-- " + self.msg)
        to.write("\n--\n")

    @staticmethod
    def responsibility(parent, line):
        return line.startswith("-- ")
    
    def __eq__(self, other):
        return isinstance(other, DayMultiBullet) and other.msg == self.msg
    
@dayactivity
class DayDone(DayActivity):
    """Mark a TODO as done.  Format is "- done: #NN" where NN is the todo number.
    """
    
    def __init__(self, seq, msg=None):
        self.seq = int(seq)
        self.msg = msg
    
    def dump(self, to):
        to.write("- done: #%d" % self.seq)
        if self.msg:
            to.write(self.msg)
        to.write("\n")
        
    @staticmethod
    def responsibility(parent, line):
        return line.startswith("- done:")

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
        if seq != None:
            self.seq = int(seq)
            DayTodo.highwatermark = max (DayTodo.highwatermark, self.seq)
        else:
            self.seq = None

        self.msg = msg
        
    def __eq__(self, other):
        return isinstance(other, DayTodo) and self.seq == other.seq and other.msg == self.msg
    
    @staticmethod
    def carryforward(fromweek, toweek):
        carryover = find_todos_in_week(fromweek)

        for c in carryover:
            toweek.entries.insert(0, c)
 
    def dump(self, to):
        to.write("- todo")

        if self.seq == None:
            DayTodo.highwatermark += 1
            self.seq = DayTodo.highwatermark

        to.write("(#%d)" % self.seq)
        to.write(": " + self.msg)
        to.write("\n")

    @staticmethod
    def responsibility(parent, line):
        return line.startswith("- todo")


###
# Static helper methods.
###
def find_todos_in_week(week):
    '''Return all DayTodo instances in a Week.
    
    Note this method will return both carryover and daily todo entries in the list, in the order they're found in the Week.
    '''
    
    todos = []
    
    for entry in week.entries:
        if (isinstance(entry, DayTodo)): todos.append(entry)
        
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
