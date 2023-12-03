#!/usr/bin/env python3

import sys
import os

import load_working_log
import worktime
from argparse import ArgumentParser

parser = ArgumentParser(description = "Working time evaluation")
parser.add_argument("-t", "--type", default="log", help="Input type (log)")
parser.add_argument("file", metavar="FILENAME", nargs="+", help="Working time file")
args = parser.parse_args()

if args.type != "log":
    parser.error("Type '{}' not supported".format(args.type))

for f in args.file:
    if not os.path.isfile(f):
        parser.error("File '{}' don't exist!".format(f))

data = load_working_log.raw_list(args.file[0])
for f in args.file[1:]:
    data += load_working_log.raw_list(f)

workdata = load_working_log.convert_raw_to_worktime(data)
workdata.days()
workdata.csv()
