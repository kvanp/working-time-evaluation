""" Calendar Informations
"""

import datetime

class holiday:
    def __init__(self, year, federal_state="BW"):
        fixed = {
            datetime.date(year,  1,  1) : "Neujahr"                  ,
            datetime.date(year,  1,  6) : "Heilige drei Könige"      ,
            datetime.date(year,  5,  1) : "Tag der Arbeit"           ,
            datetime.date(year, 10,  3) : "Tag der Deutschen Einheit",
            datetime.date(year, 11,  1) : "Allerheiligentag"         ,
            datetime.date(year, 12, 25) : "Erster Weihnachtstag"     ,
            datetime.date(year, 12, 26) : "zweiter Weihnachtstag"
        }
        easter_sunday = {}
        easter_sunday[2018] = datetime.date(2018, 4,  1)
        easter_sunday[2019] = datetime.date(2019, 4, 21)
        easter_sunday[2020] = datetime.date(2020, 4, 12)
        easter_sunday[2021] = datetime.date(2021, 4,  4)
        easter_sunday[2022] = datetime.date(2022, 4, 17)
        easter_sunday[2023] = datetime.date(2023, 4,  9)
        easter_sunday[2024] = datetime.date(2024, 3, 31)
        easter_sunday[2025] = datetime.date(2025, 4, 20)
        easter_sunday[2026] = datetime.date(2026, 4,  5)
        easter_sunday[2027] = datetime.date(2027, 3, 28)
        easter_sunday[2028] = datetime.date(2028, 4, 16)
        easter_sunday[2029] = datetime.date(2029, 4,  1)
        easter_sunday[2030] = datetime.date(2030, 4, 21)
        easter_sunday[2031] = datetime.date(2031, 4, 13)
        easter_sunday[2032] = datetime.date(2032, 3, 28)
        floating = {
            easter_sunday[year] + datetime.timedelta(days=-2) : "Karlfreitag"       ,
            easter_sunday[year]                               : "Ostersonntag"      ,
            easter_sunday[year] + datetime.timedelta(days=1)  : "Ostermontag"       ,
            easter_sunday[year] + datetime.timedelta(days=39) : "Christihimmelfahrt",
            easter_sunday[year] + datetime.timedelta(days=49) : "Pfingstsonntag"    ,
            easter_sunday[year] + datetime.timedelta(days=50) : "Pfingstmontag"     ,
            easter_sunday[year] + datetime.timedelta(days=60) : "Fronleichnam"      ,
        }
        self.federal_state = "Baden-Württemberg"
        self.days = fixed
        self.days.update(floating)
    def is_holiday(self, date):
        return date in self.days.keys()

class month:
    def __init__(self, year, month):
        self.month = month
        self.year = year
        self.creat_weekdays()
    def days(self):
        if self.month >= 12:
            return (datetime.date(self.year + 1, 1, 1) - datetime.timedelta(days=1)).day
        return (datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(days=1)).day
    def creat_weekdays(self):
        self.weekdays = {}
        for d in range(1, self.days() + 1):
            day = datetime.date(self.year, self.month, d)
            name = day.strftime("%A")
            if name in self.weekdays.keys():
                self.weekdays[name] += 1
            else:
                self.weekdays[name] = 1
