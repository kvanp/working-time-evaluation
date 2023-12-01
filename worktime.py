""" Working time stamp entry
    start date time, end date time, entry type
"""

import enum
import datetime
import utils
import cal

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
    def get_minute_rounded(self, part=15):
        minute = self.time.hour * 60 + self.time.minute
        return utils.round_int_uni(minute, 60, part)
    def get_hour_rounded(self, part=15):
        return self.get_minute_rounded(part) / 60
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
        h_morning = 0
        hours = 0
        h_next_day = 0
        early_end = -1
        midnight = 24 * 60
        start = start.hour * 60 + start.minute
        end = end.hour * 60 + end.minute

        if end <= start:
            early_end = end
            end += midnight

        for t in self.times:
            cur = t.get_minute_rounded()
            if last and t.is_working_hours_end():
                if cur < last:
                    cur += 24 * 60

                if cur < start and last > early_end or last > end:
                    last = 0
                    continue

                if last < early_end:
                    if cur < early_end:
                        hours += cur - last
                        h_morning += cur - last
                    else:
                        hours += early_end - last
                        h_morning += early_end - last

                    if cur < start:
                        last = 0
                        continue

                if cur > midnight:
                    h_next_day += cur - midnight

                if last < start:
                    last = start
                elif cur > end:
                    cur = end

                hours += cur - last
                last = 0
            elif t.is_working_hours_start():
                last = cur
        return { "hours" : hours / 60,
                    "in morning" : h_morning / 60,
                    "on next day" : h_next_day / 60}
    def get_hours(self):
        last = -1
        hours = 0

        for t in self.times:
            cur = t.get_minute_rounded()
            if last >= 0 and t.is_working_hours_end():
                if cur < last:
                    cur += 24 * 60
                hours += cur - last
                last = -1
            elif t.is_working_hours_start():
                last = cur
        return hours / 60
    def times_csv(self, sep=";"):
        string = ""
        times = self.times[::-1]
        while times:
            if len(times) == 2:
                string += "{}{s}{s}{s}{s}{}".format(times.pop(), times.pop(), s=sep)
            elif len(times) >= 4:
                string += "{}{s}{}{s}/{s}{}{s}{}".format(times.pop(), times.pop(), times.pop(), times.pop(), s=sep)
                if times:
                    string += "\n;"
        return string
    def __str__(self):
        string = ""
        times = self.times[::-1]
        while times:
            if len(times) == 2:
                string += "{}       -       {}".format(times.pop(), times.pop())
            elif len(times) >= 4:
                string += "{}-{} / {}-{}".format(times.pop(), times.pop(), times.pop(), times.pop())
                if times:
                    string += "\n                    "
        return string

class stamp_day(stamp_times):
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.sunday = date.weekday() == 6
        calender = cal.holiday(date.year)
        self.holiday = calender.is_holiday(date)
    def __lt__(self, other):
        return self.date < other.date
    def __str__(self):
        return "{}: {}".format(self.date.strftime("%a, %d. %b. %Y"), super().__str__())

class stamp_hours(stamp_day):
    def __init__(self, date):
        super().__init__(date)
        self.hours       = 0
        self.evening     = 0
        self.night       = 0
        self.sun_holiday = 0
    def __str__(self):
        return "{}: {:5.2f}".format(super().__str__(), self.get_hours())

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
    def calc_hours(self):
        evening_data = self.list[0].get_hours_in(datetime.time(20,0,0), datetime.time(0,0,0))
        day_data     = self.list[0].get_hours_in(datetime.time( 0,0,0), datetime.time(0,0,0))
        night_data   = self.list[0].get_hours_in(datetime.time(23,0,0), datetime.time(6,0,0))
        last_date    = self.list[0].date

        for e in self.list:
            sun_holiday = 0

            if (e.date - last_date).days == 1:
                day     =     day_data["on next day"]
                evening = evening_data["on next day"]
                night   =   night_data["hours"] - night_data["in morning"]
            else:
                evening = 0
                day     = 0
                night   = 0

            day_data     = e.get_hours_in(datetime.time( 0,0,0), datetime.time(0,0,0))
            evening_data = e.get_hours_in(datetime.time(20,0,0), datetime.time(0,0,0))
            night_data   = e.get_hours_in(datetime.time(23,0,0), datetime.time(6,0,0))
            day     +=     day_data["hours"]
            evening += evening_data["hours"]
            night   +=   night_data["in morning"]

            if night < 2:
                night = 0
            if e.sunday or e.holiday:
                sun_holiday = day

            last_date = e.date
            e.hours       = e.get_hours()
            e.evening     = evening
            e.night       = night
            e.sun_holiday = sun_holiday
    def output(self, all_=False, month=10, year=datetime.datetime.now().year):
        self.calc_hours()
        sum_hours       = 0
        sum_evening     = 0
        sum_nigth       = 0
        sum_sun_holiday = 0

        for e in self.list:
            if all_ or e.date.year == year and e.date.month == month:
                print(e, "| (E {:5.2f}; N {:5.2f}; S/F {:5.2f})".format(e.evening, e.night, e.sun_holiday))
                sum_hours       += e.hours
                sum_evening     += e.evening
                sum_nigth       += e.night
                sum_sun_holiday += e.sun_holiday
        print("                                              {:6.2f} | (E{:6.2f}; N{:6.2f}; S/F{:6.2f})".format(sum_hours, sum_evening, sum_nigth, sum_sun_holiday))
    def csv(self, all_=False, month=10, year=datetime.datetime.now().year, sep=";"):
        self.calc_hours()
        sum_hours       = 0
        sum_evening     = 0
        sum_nigth       = 0
        sum_sun_holiday = 0

        for e in self.list:
            if all_ or e.date.year == year and e.date.month == month:
                print(sep.join([e.date.strftime("%d.%m.%Y"), e.times_csv(sep), "{:.2f}".format(e.hours), "(A {:5.2f}| N {:5.2f}| S/F {:5.2f})".format(e.evening, e.night, e.sun_holiday)]))
                sum_hours       += e.hours
                sum_evening     += e.evening
                sum_nigth       += e.night
                sum_sun_holiday += e.sun_holiday
        print("{s}{s}{s}{s}{s}{s}{:.2f}{s}(A{:6.2f}| N{:6.2f}| S/F{:6.2f})".format(sum_hours, sum_evening, sum_nigth, sum_sun_holiday, s=sep))
    def days(self):
        self.output()
