'''
A model to describe a week in the life of pyd.

Each model class implements dump().

'''


class Week:
    
    def __init__(self, year):
        self.entries = list()
        self.year = year
    
    def days(self):
        def is_day(entry): return isinstance(entry, Day)    
        return filter(is_day, self.entries)
        
    def dump(self, to):
        for entry in self.entries:
            entry.dump(to)
    

class WeekEntry(object):
    """Abstract class from which all things in a week are derived.
    
        Usually a week just has Day objects in it, however directly referencing Day runs into a challenge
        where there may be other kinds of entries (such as freeform text) that we don't want to lose.
    """
    def dump(self, to):
        pass
    
class FreeformWeekEntry(object):
    """Generic place holder for "things we found in the file that aren't something else."""
    
    def __init__(self, text):
        self.text = text
        
    def dump(self, to):
        to.write(self.text + "\n")

class Day(object):
    """A day contains DayActivities and some metadata.
    
    A day knows which year its in from the Week.
    """
    
    def add_activity(self, act):
        self.activities.append(act)

    def todos(self):
        def is_todo(entry): return isinstance(entry, DayTodo)    
        return filter(is_todo, self.activities)
    
    def dones(self):
        def is_done(entry): return isinstance(entry, DayDone)    
        return filter(is_done, self.activities)
        
    def __init__(self, my_day):
        self.my_day = my_day
        self.activities = list()
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

class DayBullet(DayActivity):
    """A thing you did today.  Starts with "- " and contains a single line of text.
    """
    
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("- " + self.msg)
        to.write("\n")

class DayMultiBullet(DayActivity):
    """A thing you did today; supporting multiple lines.  
    
    Starts with "--" (followed optionally by text) and ends with "--" on a line by itself.
    """
    
    def __init__(self, msg):
        self.msg = msg

    def dump(self, to):
        to.write("-- " + self.msg)
        to.write("\n--\n")
    
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
        
            
    def dump(self, to):
        to.write("- todo")

        if self.seq == None:
            DayTodo.highwatermark += 1
            self.seq = DayTodo.highwatermark

        to.write("(#%d)" % self.seq)
        to.write(": " + self.msg)
        to.write("\n")
