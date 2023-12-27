"""Working time stamp entry
start date time, end date time, entry type
"""

import enum
import datetime
import utils
import cal

class enum_stamp_type(enum.Enum):
    """Enum of Entry types"""
    none_of_work        = enum.auto()
    start_of_work       = enum.auto()
    start_of_work_break = enum.auto()
    end_of_work_break   = enum.auto()
    end_of_work         = enum.auto()
    def __lt__(self, other):
        return self.value < other.value

class stamp_time:
    """Single stamp time with type"""
    def __init__(self, time, stype):
        """
        Arguments:
        time  -- the time as a `datetime.time` object
        stype -- the type of the time as `enum_stamp_type`
        """
        self.time = time
        self.stamp_type = stype
    def get_minute(self):
        """Get the time in minutes
        Return: minutes
        """
        return self.time.hour * 60 + self.time.minute
    def get_minute_rounded(self, part=15):
        """Get the time in minutes and rounded
        Arguments:
        part -- step with for the rounding in minutes (default 15)

        Return: minutes
        """
        minute = self.time.hour * 60 + self.time.minute
        return utils.round_int_uni(minute, 60, part)
    def get_hour_rounded(self, part=15):
        """Get the time in hours and rounded
        Arguments:
        part -- step with for the rounding in minutes (default 15)

        Return: hours
        """
        return self.get_minute_rounded(part) / 60
    def rounded_quater_hour(self):
        """Get the time in minutes and rounded to 15 minutes

        Return: minutes
        """
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
        """Is true if the time is start of working"""
        return self.stamp_type == enum_stamp_type.start_of_work
    def is_start_of_work_break(self):
        """Is true if the time is start pause"""
        return self.stamp_type == enum_stamp_type.start_of_work_break
    def is_end_of_work_break(self):
        """Is true if the time is end of pause"""
        return self.stamp_type == enum_stamp_type.end_of_work_break
    def is_end_of_work(self):
        """Is true if the time is end of working"""
        return self.stamp_type == enum_stamp_type.end_of_work
    def is_working_hours_start(self):
        """Is true if the time is start of working"""
        return self.is_start_of_work() or self.is_end_of_work_break()
    def is_working_hours_end(self):
        """Is true if the time is end of working"""
        return self.is_start_of_work_break() or self.is_end_of_work()
    def __lt__(self, other):
        if self.time < other.time and self.stamp_type > other.stamp_type:
            return False
        return self.time < other.time
    def __str__(self):
        return self.rounded_quater_hour().strftime("%H:%M")

class stamp_times:
    """List of time stamps as `stamp_time`"""
    def __init__(self):
        self.times = []
    def append(self, time, stype):
        """Add a time to the list
        Arguments:
        time  -- the time as `datetime.time`
        stype -- the type of the time as `enum_stamp_type`
        """
        self.times.append(stamp_time(time,stype))
        self.times.sort()
    def get_hours_in(self, start, end):
        """Get the hours where between start and end
        Argumnets:
        start -- the start time as `datetime.time`
        start -- the end time as `datetime.time`
        Return: hours
        """
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
        """Indicates the hours worked as hours"""
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
        """Print the time list in csv format
        Argument:
        sep -- the separator for the csv output (default ';')
        Return: string
        """
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
        if not times:
            string = "                         "
        while times:
            if len(times) == 2:
                string += "{}       -       {}".format(times.pop(), times.pop())
            elif len(times) >= 4:
                string += "{}-{} / {}-{}".format(times.pop(), times.pop(), times.pop(), times.pop())
                if times:
                    string += "\n                    "
        return string

class stamp_day(stamp_times):
    """Add the date to the list of time stamps"""
    def __init__(self, date):
        """
        Arguments:
        date -- the date as `datetime.date`
        """
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
    """Time stamps for a day"""
    def __init__(self, date):
        """
        Arguments:
        date -- the date as `datetime.date`
        """
        super().__init__(date)
        self.hours        = 0
        self.evening      = 0
        self.night        = 0
        self.sun_holiday  = 0
        self.target_hours = 0
    def __str__(self):
        return "{}: {:7.2f} {:7.2f}".format(super().__str__(), self.target_hours, self.get_hours())

class raw_list:
    """A empty skeleton for the input types"""
    def create(self, file_):
        """Create a new raw list

        Arguments:
        file_ -- path/filename to the logfile
        """
        pass
    def append(self, file_):
        """Appand entrys to the raw list

        Arguments:
        file_ -- path/filename to the logfile
        """
        pass
    def convert(self):
        """Convert the raw list to the worktime list type"""
        return list()

class list:
    """A list of time stamps grouped by day"""
    def __init__(self):
        self.list = []
        self.should = [8,8,8,8,8,0,0]
    def append(self, date_time, stype):
        """Add new element to the list
        Arguments:
        date_time -- the date and time of a stamp as a `datetime.time` object
        stype     -- the type of the stamp as `enum_stamp_type`
        """
        for e in self.list:
            if e.date == date_time.date():
                if not e.times and (stype == enum_stamp_type.start_of_work_break or stype == enum_stamp_type.end_of_work):
                    self.append(date_time - datetime.timedelta(days=1), stype)
                else:
                    e.append(date_time.time(), stype)

                break
        else:
            month = cal.month(date_time.year, date_time.month)
            list_ = []

            for d in range(1, month.days()+1):
                day = stamp_hours(datetime.date(date_time.year, date_time.month, d))

                if day.holiday:
                    day.target_hours = self.should[6]
                else:
                    day.target_hours = self.should[day.date.weekday()]

                list_.append(day)

            self.list += list_
            self.append(date_time, stype)

    def calc_hours(self):
        """Calculate some informations per day
        - hours in the evening between 20 o'clock and 24 o'clock
        - hours in the night between 23 o'clock and 6 o'clock if this are 2 hours and more
        - hours in on sun- and holidays
        """
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
    def total(self, format_=None):
        """Output of totals"""

        self.calc_hours()
        sums = {}

        for e in self.list:
            if format_:
                idx = e.date.strftime(format_)
            else:
                idx = "Total"

            if not idx in sums.keys():
                sums[idx] = {"hours" : 0, "evening" : 0, "night" : 0, "sun_holiday" : 0}

            sums[idx]["hours"]       += e.hours
            sums[idx]["evening"]     += e.evening
            sums[idx]["night"]       += e.night
            sums[idx]["sun_holiday"] += e.sun_holiday

        for k,v in sums.items():
            print("{} {:7.2f} | (E{:6.2f}; N{:6.2f}; S/H{:6.2f})".format(k, v["hours"], v["evening"], v["night"], v["sun_holiday"]))

class output:
    """Some output variants"""
    def text(self, cls, month=-1, year=None):
        """Print a nice of the data
        Arguments:
        month -- the month for the output if '-1' output all (default -1)
        year  -- the year for the output (default None)
        """
        if not cls.list:
            return

        cls.calc_hours()
        sum_hours       = 0
        sum_evening     = 0
        sum_nigth       = 0
        sum_sun_holiday = 0

        if year == None:
            year = datetime.datetime.now().year

        for e in cls.list:
            if month == -1 or e.date.year == year and e.date.month == month:
                print(e, "| (E {:6.2f}; N {:6.2f}; S/H {:6.2f})".format(e.evening, e.night, e.sun_holiday))
                sum_hours       += e.hours
                sum_evening     += e.evening
                sum_nigth       += e.night
                sum_sun_holiday += e.sun_holiday
        print("Total                                          {:7.2f} | (E {:6.2f}; N {:6.2f}; S/H {:6.2f})".format(sum_hours, sum_evening, sum_nigth, sum_sun_holiday))
    text = classmethod(text)

    def csv(self, cls, month=-1, year=None, sep=";"):
        """Print the data in csv format
        Arguments:
        month -- the month for the output if '-1' output all (default -1)
        year  -- the year for the output (default None)
        sep   -- the separator (default ';')
        """
        if not cls.list:
            return

        cls.calc_hours()
        sum_hours       = 0
        sum_evening     = 0
        sum_nigth       = 0
        sum_sun_holiday = 0

        if year == None:
            year = datetime.datetime.now().year

        for e in cls.list:
            if month == -1 or e.date.year == year and e.date.month == month:
                print(sep.join([e.date.strftime("%d.%m.%Y"), e.times_csv(sep), "{:.2f}".format(e.hours), "(E {:.2f}| N {:.2f}| S/H {:.2f})".format(e.evening, e.night, e.sun_holiday)]))
                sum_hours       += e.hours
                sum_evening     += e.evening
                sum_nigth       += e.night
                sum_sun_holiday += e.sun_holiday
        print("Total{s}{s}{s}{s}{s}{s}{:.2f}{s}(E {:.2f}| N {:.2f}| S/H {:.2f})".format(sum_hours, sum_evening, sum_nigth, sum_sun_holiday, s=sep))
    csv = classmethod(csv)

    def total(self, cls):
        """Output of totals"""
        cls.total()
    total = classmethod(total)

    def year(self, cls):
        """Output of yearly totals"""
        cls.total("%Y")
    year = classmethod(year)

    def month(self, cls):
        """Output of monthly totals"""
        cls.total("%Y %b")
    month = classmethod(month)
