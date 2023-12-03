#!/usr/bin/env python3

from os import path
from argparse import ArgumentParser

import load_working_log
import worktime

parser = ArgumentParser(description = "Working time evaluation")
parser.add_argument("-t", "--type" , default="log", help="Input type (log)")
parser.add_argument("-y", "--year" , type=int   , help="Year")
parser.add_argument("-m", "--month", type=int, default=-1 , help="Month")
parser.add_argument("file", metavar="FILENAME", nargs="+", help="Working time file")
args = parser.parse_args()

if args.type != "log":
    parser.error("Type '{}' not supported".format(args.type))

if args.month != -1 and args.month < 1 or args.month > 12:
    parser.error("Month 1...12")

for f in args.file:
    if not path.isfile(f):
        parser.error("File '{}' don't exist!".format(f))

data = load_working_log.raw_list(args.file[0])
for f in args.file[1:]:
    data += load_working_log.raw_list(f)

workdata = load_working_log.convert_raw_to_worktime(data)
workdata.days(args.month, args.year)
workdata.csv(args.month, args.year)
