""" Working time stamp entry
    start date time, end date time, entry type
"""

import enum
import datetime

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

        for stamp in self.list:
            start = (   stamp.wtype == enum_worktime.start_of_work or
                        stamp.wtype == enum_worktime.end_of_work_break)
            end = ( stamp.wtype == enum_worktime.end_of_work or
                    stamp.wtype == enum_worktime.start_of_work_break)
            date_str_tmp = stamp.date_time.strftime("%a, %d. %b. %Y")
            time = stamp.date_time
            # Auf viertel Stunde runden
            sec = (((time.minute + 7) * 4 // 60) * 15 - time.minute) * 60
            time += datetime.timedelta(seconds=sec)
            time_str = time.strftime("%H:%M")

            if date_str and start and date_str != date_str_tmp:
                line["hours"] = "{}".format(line["hours"].seconds / 3600)
                print(line)
                line["times"] = []
                line["hours"] = datetime.timedelta(minutes=0)

            if start:
                line["date"] = date_str_tmp
                date_str = date_str_tmp
                time_start = time
            elif not date_str:
                continue
            if end:
                line["hours"] += time - time_start

            line["times"].append(time_str)

        print(line)
