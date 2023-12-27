"""Load worktimes from a Excel sheet"""

import worktime
from openpyxl import load_workbook

def quick_hack(filename):
    wb = load_workbook(filename=filename)
    sheet = wb[wb.sheetnames[0]]
    offset = 5

    while sheet.cell(offset, 1).value:
        line = [
            sheet.cell(offset, 1).value,
            sheet.cell(offset, 2).value,
            sheet.cell(offset, 3).value,
            sheet.cell(offset, 5).value,
            sheet.cell(offset, 6).value,
        ]
        print(str(line))
        offset += 1
        if offset > sheet.max_row:
            break

class list(worktime.raw_list):
    """List of worktime entrys from .xlsx file"""
    def create(self, file_):
        """Create a new raw list

        Arguments:
        file_ -- path/filename to the logfile
        """
        quick_hack(file_)
    def append(self, file_):
        """Appand entrys to the raw list

        Arguments:
        file_ -- path/filename to the logfile
        """
        pass
    def convert(self):
        """Convert the raw list to the worktime list type"""
        return worktime.list()

