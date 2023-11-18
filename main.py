#!/usr/bin/env python3

import sys

import load_working_log
import worktime

filename = "Arbeitsprotokoll.log"
data = load_working_log.raw_list(filename)
data.output()
