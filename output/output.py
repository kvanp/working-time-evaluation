import datetime
#import worktime

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
        sum_hours           = 0
        sum_evening         = 0
        sum_nigth           = 0
        sum_sun_holiday     = 0
        sum_target_hours    = 0
        sum_overtime        = 0
        sum_vacation        = 0
        sum_unpait_vacation = 0
        sum_ill             = 0

        if year == None:
            year = datetime.datetime.now().year

        for e in cls.list:
            if month == -1 or e.date.year == year and e.date.month == month:
                sum_overtime += e.overtime
                stat = ""
                if e.holiday:
                    stat += "H"
                if e.e_correction:
                    stat += "C"
                if stat:
                    stat = " " + stat
                print(e, "{:7.2f} {:7.2f}| (E {:6.2f}; N {:6.2f}; S/H {:6.2f}){}".format(
                    e.overtime, sum_overtime, e.evening, e.night, e.sun_holiday, stat))
                sum_hours        += e.hours
                sum_evening      += e.evening
                sum_nigth        += e.night
                sum_sun_holiday  += e.sun_holiday
                sum_target_hours += e.target_hours
                if e.target_hours:
                    if e.day_meta["vacation"       ]:
                        sum_vacation += 1
                    if e.day_meta["unpaid_vacation"]:
                        sum_unpaid_vacation += 1
                    if e.day_meta["ill"            ]:
                        sum_ill += 1
        print("Total                                          {:7.2f} {:7.2f} {:7.2f}        | (E {:6.2f}; N {:6.2f}; S/H {:6.2f}) V {:2} I {:2} UV {:2}".format(
            sum_hours, sum_target_hours, sum_overtime, sum_evening, sum_nigth, sum_sun_holiday, sum_vacation, sum_ill, sum_unpait_vacation))
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
        cls.total()
    year = classmethod(year)

    def month(self, cls):
        """Output of monthly totals"""
        cls.total("%Y %b")
        cls.total("%Y")
        cls.total()
    month = classmethod(month)
