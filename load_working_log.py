"""Load protokol
Read the log entrys from the logfile and creat a tuble of work time
"""

from datetime import datetime

import worktime

class dataset:
    """ Data struct from one entry

    Arguments:
    date_time -- the data and time of the entry as datetime object
    place     -- the place where you were at the time
    subject   -- the subject of your work
    comment   -- what you have done
    """
    def __init__(self, date_time, place, subject, comment):
        """dataset(date_time, place, subject, comment)
        Arguments:
        date_time -- the data and time of the entry as datetime object
        place     -- the place where you were at the time
        subject   -- the subject of your work
        comment   -- what you have done
        """
        self.date_time = date_time
        self.place     = place
        self.subject   = subject
        self.comment   = comment
    def show(self):
        """Output of the storge"""
        print("{}|{}|{}|{}".format(self.date_time, self.place, self.subject, self.comment))
    def is_end(self):
        """lets you know whether it is an ENDE entry"""
        _end = "END"
        if self.place.upper() == _end or self.subject.upper() == _end:
            return True
        return False
    def is_pause(self):
        """lets you know whether it is an PAUSE entry"""
        _end = "PAUSE"
        if self.place.upper() == _end or self.subject.upper() == _end:
            return True
        return False
    def is_privat(self):
        """lets you know whether it is an PRIVAT entry"""
        if self.place.upper() == "PRIVAT" or self.subject.upper() == "PRIVAT" or (self.comment and self.comment[0] == '!'):
            return True
        return False
        pass

class fix_line:
    """Defines the fixed columns and returns the individual attributes"""
    def date_time(str_):
        """Get the date and time of the entry

        Arguments:
        str_ -- line of a protokol entry
        """
        return datetime.strptime(str_[0:17].strip(), "%Y-%m-%d %H:%M")
    def place(str_):
        """Get the place of the entry

        Arguments:
        str_ -- line of a protokol entry
        """
        return str_[17:40].strip()
    def subject(str_):
        """Get the subject of the entry

        Arguments:
        str_ -- line of a protokol entry
        """
        return str_[40:64].strip()
    def comment(str_):
        """Get the comment of the entry

        Arguments:
        str_ -- line of a protokol entry
        """
        return str_[64:].strip()

def loader(filename):
    """loader(filename)
    Read a logfile

    Arguments:
    filename -- path/filename to the logfile

    Return: a list of `dataset` objects
    """
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
    """Store the lines read in"""
    def __init__(self, filename):
        """
        Arguments:
        filename -- path/filename to the logfile
        """
        self.list = loader(filename)
    def append(self, date_time, place, subject, comment):
        """Add a new line to the list"""
        self.list.append(dataset(date_time, place, subject, comment))
    def output(self):
        """Print the storge"""
        for d in self.list:
            d.show()

def convert_raw_to_worktime(raw_list):
    """convert the log entrys to the worktime data struct

    Arguments:
    raw_list --- list whit dataset objects

    Return: `worktime.list` object
    """
    start = False
    pause = False
    working_time_list = worktime.list()

    for entry in raw_list.list:
        if not start and not pause and not entry.is_end() and not entry.is_pause() and not entry.is_privat():
            start = True
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.start_of_work)
        elif start and not pause and entry.is_pause():
            pause = True
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.start_of_work_break)
        elif start and pause and not entry.is_end() and not entry.is_pause() and not entry.is_privat():
            pause = False
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.end_of_work_break)
        elif start and not pause and entry.is_end():
            start = False
            working_time_list.append(entry.date_time, worktime.enum_stamp_type.end_of_work)

    return working_time_list
