""" Working time stamp entry
    start date time, end date time, entry type
"""

import enum
import datetime
import utils

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
        if not isinstance(self.date_time, datetime.datetime):
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
    def is_start_of_work(self):
        return self.wtype == enum_worktime.start_of_work
    def is_start_of_work_break(self):
        return self.wtype == enum_worktime.start_of_work_break
    def is_end_of_work_break(self):
        return self.wtype == enum_worktime.end_of_work_break
    def is_end_of_work(self):
        return self.wtype == enum_worktime.end_of_work
    def is_working_hours_start(self):
        return self.is_start_of_work() or self.is_end_of_work_break()
    def is_working_hours_end(self):
        return self.is_start_of_work_break() or self.is_end_of_work()
    def time_rounded_quater_hour(self):
        sec = utils.round_int_uni_difference(self.date_time.minute, 60, 15) * 60
        return self.date_time + datetime.timedelta(seconds=sec)

class list:
    def __init__(self):
        self.list = []
    def append(self, date_time, wtype):
        self.list.append(worktime(date_time, wtype))
    def output(self):
        for e in self.list:
            e.view()
    def days(self):
        date_str = ""
        line = {"date" : "", "times" : [], "hours" : datetime.timedelta(minutes=0)}
        hours = datetime.timedelta(hours=0)

        for stamp in self.list:
            date_str_tmp = stamp.date_time.strftime("%a, %d. %b. %Y")
            time = stamp.time_rounded_quater_hour()
            time_str = time.strftime("%H:%M")

            if date_str and stamp.is_working_hours_start() and date_str != date_str_tmp:
                line["hours"] = "{}".format(hours.seconds / 3600)
                print(line)
                line["times"] = []
                hours = datetime.timedelta(hours=0)

            if stamp.is_working_hours_start():
                line["date"] = date_str_tmp
                date_str = date_str_tmp
                time_start = time
            elif not date_str:
                continue
            if stamp.is_working_hours_end():
                hours += time - time_start

            line["times"].append(time_str)

        if hours != datetime.timedelta(hours=0):
            line["hours"] = "{}".format(hours.seconds / 3600)

        print(line)
