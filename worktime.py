""" Working time stamp entry
    start date time, end date time, entry type
"""

import enum
import datetime
import utils

class enum_stamp_type(enum.Enum):
    """ Entry type
    """
    none_of_work        = enum.auto()
    start_of_work       = enum.auto()
    start_of_work_break = enum.auto()
    end_of_work_break   = enum.auto()
    end_of_work         = enum.auto()
    def __lt__(self, other):
        return self.value < other.value

class stamp_time:
    def __init__(self, time, stype):
        self.time = time
        self.stamp_type = stype
    def get_minute(self):
        return self.time.hour * 60 + self.time.minute
    def get_minute_rouded(self, part=15):
        minute = self.time.hour * 60 + self.time.minute
        return utils.round_int_uni(minute, 60, part)
    def rounded_quater_hour(self):
        hour = self.time.hour
        minute = utils.round_int_uni(self.time.minute, 60, 15)
        if minute >= 60:
            hour += 1
            if hour >= 24:
                hour = 0
            minute = minute - 60
        return self.time.replace(hour=hour, minute=minute)
        #sec = utils.round_int_uni_difference(self.time.minute, 60, 15) * 60
        #return self.time + datetime.timedelta(seconds=sec)
    def is_start_of_work(self):
        return self.stamp_type == enum_stamp_type.start_of_work
    def is_start_of_work_break(self):
        return self.stamp_type == enum_stamp_type.start_of_work_break
    def is_end_of_work_break(self):
        return self.stamp_type == enum_stamp_type.end_of_work_break
    def is_end_of_work(self):
        return self.stamp_type == enum_stamp_type.end_of_work
    def is_working_hours_start(self):
        return self.is_start_of_work() or self.is_end_of_work_break()
    def is_working_hours_end(self):
        return self.is_start_of_work_break() or self.is_end_of_work()
    def __lt__(self, other):
        if self.time < other.time and self.stamp_type > other.stamp_type:
            return False
        return self.time < other.time
    def __str__(self):
        return self.rounded_quater_hour().strftime("%H:%M")

class stamp_times:
    def __init__(self):
        self.times = []
    def append(self, time, stype):
        self.times.append(stamp_time(time,stype))
        self.times.sort()
    def get_hours_in(self, start, end):
        last = 0
        hours = 0
        start = start.hour * 60 + start.minute
        end = end.hour * 60 + end.minute

        if end < start:
            end += 24 * 60

        for t in self.times:
            cur = t.get_minute_rouded()
            if last and t.is_working_hours_end():
                if cur < last:
                    cur += 24 * 60

                if cur < start or last > end:
                    continue
                elif last < start:
                    last = start
                elif cur > end:
                    cur = end

                hours += cur - last
                last = 0
            elif t.is_working_hours_start():
                last = cur
        return datetime.time(hours // 60, hours % 60)
    def get_hours(self):
        last = 0
        hours = 0

        for t in self.times:
            cur = t.get_minute_rouded()
            if last and t.is_working_hours_end():
                if cur < last:
                    cur += 24 * 60
                hours += cur - last
                last = 0
            elif t.is_working_hours_start():
                last = cur
        return datetime.time(hours // 60, hours % 60)
    def __str__(self):
        string = []
        for t in self.times:
            string += [str(t)]
        return "{:82}".format('; '.join(string))

class stamp_day(stamp_times):
    def __init__(self, date):
        super().__init__()
        self.date = date
    def __lt__(self, other):
        return self.date < other.date
    def __str__(self):
        return "{}: {}".format(self.date.strftime("%a, %d. %b. %Y"), super().__str__())

class stamp_hours(stamp_day):
    def __init__(self, date):
        super().__init__(date)
    def __str__(self):
        return "{}: {}".format(super().__str__(), self.get_hours())

class list:
    def __init__(self):
        self.list = []
    def append(self, date_time, stype):
        for e in self.list:
            if e.date == date_time.date():
                e.append(date_time.time(), stype)
                break
        else:
            if stype == enum_stamp_type.start_of_work_break or stype == enum_stamp_type.end_of_work:
                self.append(date_time - datetime.timedelta(days=1), stype)
            else:
                tmp = stamp_hours(date_time.date())
                tmp.append(date_time.time(), stype)
                self.list.append(tmp)
    def output(self):
        for e in self.list:
            print(e, "| {}".format(e.get_hours_in(datetime.time(18,0,0), datetime.time(0,0,0))))
    def days(self):
        self.output()
