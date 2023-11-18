""" Working time stamp entry
    start date time, end date time, entry type
"""

import enum
from datetime import datetime

class enum_worktime(enum.Enum):
    """ Entry type
    """
    start_of_work       = enum.auto()
    start_of_work_break = enum.auto()
    end_of_work_break   = enum.auto()
    end_of_work         = enum.auto()

class worktime:
    """ Work time entry
        Single entry
    """
    def __init__(self, date_time, wtype):
        self.date_time = date_time
        self.wtype = wtype
    def view(self):
        print("At {} is {}".format(self.date_time, self.wtype))
    def check(self):
        err = {}
        if not isinstance(self.date_time, datetime):
            err["Start"] = 'datetime.datetime'
        if not isinstance(self.wtype, enum_worktime):
            err["Type"]  = 'enum_worktime'

        if err:
            for k, v in err.items():
                print("{} is not datatype '{}'".format(k, v))
            return False

        if not err:
            print("All is fine")
            return True

class list:
    def __init__(self):
        self.list = []
    def append(self, date_time, wtype):
        self.list.append(worktime(date_time, wtype))
    def output(self):
        for e in self.list:
            e.view()
