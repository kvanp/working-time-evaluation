#!/usr/bin/env python3

from os import path
from argparse import ArgumentParser

import version
import load_working_log
import load_sheet_month
import worktime

class input_type:
    """Class array for the input types

    The skeleton is defined under 'worktime.raw_list'.
    """
    objs = {
        "log"  : load_working_log.list,
#        "org"  : worktime.raw_list,     # Dummy for future use
        "xlsx" : load_sheet_month.list,
    }
    def __str__(self):
        return "Input type ({})".format(", ".join(self.objs.keys()))

class output_type:
    """Class array for the output types"""
    objs = {
        "text"  : worktime.output.text,
        "csv"   : worktime.output.csv,
    }
    def __str__(self):
        return "Output type ({})".format(", ".join(self.objs.keys()))

class data_type:
    """Class array for the output types"""
    objs = {
        "total"  : worktime.output.total,
        "year"   : worktime.output.year,
        "month"  : worktime.output.month,
    }
    def __str__(self):
        return "Data type ({})".format(", ".join(self.objs.keys()))

parser = ArgumentParser(description = "Working time evaluation")
parser.add_argument("-V", "--version" , action="version", version=str(version.version))
parser.add_argument("-t", "--type" , default="log", help=str(input_type()))
parser.add_argument("-o", "--output-type" , help=str(output_type()))
parser.add_argument("-d", "--data-type" , help=str(data_type()))
parser.add_argument("-y", "--year" , type=int   , help="Year")
parser.add_argument("-m", "--month", type=int, default=-1 , help="Month")
parser.add_argument("-s", "--should", help="Comma-separated list of target hours per weekday. Starting with Monday. (Default '8,8,8,8,8,8,0,0')")
parser.add_argument("-a", "--annual-vacation" , type=int, default=0  , help="Annual Vacation")
parser.add_argument("-r", "--remaining-vacation-to-hours" , action="store_true"   , help="Convert remaining vacation into hours")
parser.add_argument("file", metavar="FILENAME", nargs="+", help="Working time file")
args = parser.parse_args()

if not args.type in input_type().objs.keys():
    parser.error("Type '{}' not supported".format(args.type))

if args.output_type and not args.output_type in output_type().objs.keys():
    parser.error("Output type '{}' not supported".format(args.output_type))

if args.data_type and not args.data_type in data_type().objs.keys():
    parser.error("Data type '{}' not supported".format(args.data_type))

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
workdata.set_meta({"annual_vacation" : args.annual_vacation, "remaining_vacation_to_hours" : args.remaining_vacation_to_hours})
if args.should:
    list_ = []
    for i in args.should.split(','):
        list_.append(int(i))
    workdata.new_shoulds(list_)

if args.output_type:
    output_type.objs[args.output_type](workdata, args.month, args.year)
if args.data_type:
    data_type.objs[args.data_type](workdata)
if not args.output_type and not args.data_type:
    output_type.objs["text"](workdata, args.month, args.year)
    output_type.objs["csv"](workdata, args.month, args.year)
