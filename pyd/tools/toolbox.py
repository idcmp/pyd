"""
    SDK ontop of the API
"""

from datetime import date

from pyd.api import diaryreader as reader
from pyd.api import diarywriter as writer
from pyd.api import diarymodel as model
from pyd.api import naming
from pyd.api import carryforward as cf
from pyd.api.diarymodel import MAXIMUM_HOLIDAY_WEEKS


def find_todos_in_file(filename):
    dr = reader.DiaryReader()
    week = dr.read_file(filename)
    return model.find_todos_in_week(week)


def find_yesterday():
    """Find the last day in the diary which is not today;
     this will go back up to MAXIMUM_HOLIDAY_WEEKS if needed."""
    current_diary = naming.current_name()
    cf.perform_carryforward()
    ensure_current_header_exists(current_diary)

    days_to_go_back = 0
    yesterday = None

    while yesterday is None:
        days_to_go_back += 1
        yesterday = _try_yesterday(days_to_go_back)
        if days_to_go_back == MAXIMUM_HOLIDAY_WEEKS * 7:
            return None
    return yesterday


def _try_yesterday(days_to_go_back):
    """Private."""
    yesterday_diaryname = naming.relative_name(days_ago=days_to_go_back)

    week = reader.DiaryReader().read_file(yesterday_diaryname)

    if yesterday_diaryname == naming.current_name():
        if len(week.days()) == 0 or is_today(week.days()[0]):
            return None

        # Pair up N and N+1 in tuples, iterate through each tuple and if N+1 matches
        # today, then return N.
        for yesterday, today in zip(week.days(), week.days()[1:]):
            if is_today(today):
                return yesterday

    size = len(week.days())
    if not size:
        return None

    return week.days()[size - 1]


def ensure_current_header_exists(filename):
    """Ensures the day header for the current day exists in filename.
    
    This will read/rewrite the file to add one.
    """

    week = reader.DiaryReader().read_file(filename)

    # if we have more than one for whatever reason, that's fine.
    if len(filter(lambda day: day.my_day == date.today(), week.days())) == 0:
        day = model.Day(date.today())
        week.entries.append(day)

        writer.DiaryWriter().write_file(filename, week)


def read_and_rewrite(filename):
    """Converts a diary file to a model and back again.
    
    Used after a manual edit to the file occurs to perform any needed synchronization.
    """
    week = reader.DiaryReader().read_file(filename)
    writer.DiaryWriter().write_file(filename, week)


def is_today(day):
    """Is the passed in Day object "today" ?"""
    return model.Day(date.today()) == day
