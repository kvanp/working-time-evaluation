""" Load Arbeitslog
    Read the log entrys from the logfile and creat a tuble of work time
"""

from datetime import datetime

import worktime

class dataset:
    def __init__(self, date_time, place, subject, comment):
        self.date_time = date_time
        self.place     = place
        self.subject   = subject
        self.comment   = comment
    def show(self):
        print("{}|{}|{}|{}".format(self.date_time, self.place, self.subject, self.comment))
    def is_end(self):
        _end = "END"
        if self.place.upper() == _end or self.subject.upper() == _end:
            return True
        return False
    def is_pause(self):
        _end = "PAUSE"
        if self.place.upper() == _end or self.subject.upper() == _end:
            return True
        return False
    def is_privat(self):
        if self.place.upper() == "PRIVAT" or (self.subject and self.subject[0] == '!'):
            return True
        return False
        pass

class fix_line:
    def date_time(str_):
        return datetime.strptime(str_[0:17].strip(), "%Y-%m-%d %H:%M")
    def place(str_):
        return str_[17:40].strip()
    def subject(str_):
        return str_[40:64].strip()
    def comment(str_):
        return str_[64:].strip()

def loader(filename):
    fobj = open(filename, "r")
    ignore_line = False
    data = []

    for l in fobj:
        if not ignore_line: # We don't want the header line
            ignore_line = True
            continue

        if l[0] == '#':
            continue

        data.append(dataset(fix_line.date_time(l),
                            fix_line.place(l),
                            fix_line.subject(l),
                            fix_line.comment(l)))

    fobj.close()
    return data

class raw_list:
    def __init__(self, filename):
        self.list = loader(filename)
    def append(self, date_time, place, subject, comment):
        self.list.append(dataset(date_time, place, subject, comment))
    def output(self):
        for d in self.list:
            d.show()

def convert_raw_to_worktime(raw_list):
    start = False
    pause = False
    working_time_list = worktime.list()

    for entry in raw_list.list:
        if not start and not pause and not entry.is_end() and not entry.is_pause():
            start = True
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.start_of_work)
        if start and not pause and entry.is_pause():
            pause = True
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.start_of_work_break)
        if start and pause and not entry.is_end() and not entry.is_pause():
            pause = False
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.end_of_work_break)
        if start and not pause and entry.is_end():
            start = False
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.end_of_work)

    return working_time_list
