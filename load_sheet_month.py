"""Load worktimes from a Excel sheet"""

import worktime

class list(worktime.raw_list):
    """List of worktime entrys from .xlsx file"""
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
        return worktime.list()

