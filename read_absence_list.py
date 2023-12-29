"""Read a absence list"""

import csv
from datetime import datetime

def read(filename):
    format_ = "%d.%m.%y"
    reader = csv.reader(open(filename))

    for row in reader:
        row[1] = datetime.strptime(row[1], format_).date()

        if len(row) == 3:
            row[2] = datetime.strptime(row[2], format_).date()

    return reader
