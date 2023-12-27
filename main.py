#!/usr/bin/env python3

from os import path
from argparse import ArgumentParser

import version
import load_working_log
import worktime

class input_type:
    """Class array for the input types

    The skeleton is defined under 'worktime.raw_list'.
    """
    objs = {
        "log"  : load_working_log.list,
#        "org"  : worktime.raw_list,     # Dummy for future use
        "xlsx" : worktime.raw_list,     # Dummy for future use
    }
    def __str__(self):
        return "Input type ({})".format(", ".join(self.objs.keys()))

parser = ArgumentParser(description = "Working time evaluation")
parser.add_argument("-V", "--version" , action="version", version=str(version.version))
parser.add_argument("-t", "--type" , default="log", help=str(input_type()))
parser.add_argument("-y", "--year" , type=int   , help="Year")
parser.add_argument("-m", "--month", type=int, default=-1 , help="Month")
parser.add_argument("file", metavar="FILENAME", nargs="+", help="Working time file")
args = parser.parse_args()

if not args.type in input_type().objs.keys():
    parser.error("Type '{}' not supported".format(args.type))

if args.month != -1 and args.month < 1 or args.month > 12:
    parser.error("Month 1...12")

for f in args.file:
    if not path.isfile(f):
        parser.error("File '{}' don't exist!".format(f))

data = input_type().objs[args.type]()
data.create(args.file[0])
for f in args.file[1:]:
    data.append(f)

workdata = data.convert()
workdata.days(args.month, args.year)
workdata.csv(args.month, args.year)
