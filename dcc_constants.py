#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
ASTI SOLAR RADIATION DATA DOWNLOAD, COMPILE, AND CONVERT TOOL
-------
A Collection of Python scripts that downloads daily measurements from
weather measurment stations (WMS) from the Philippine E-Science Grid
repository <http://repo.pscigrid.gov.ph/predict>, compiles and averages
them to monthly average values, and saves the result into a shapefile.

NB:
The Tool has only been tested for *buntu (Linux) and Python 2.7.x
The requirements/modules are found in the included requirements.txt
The Tool is provided under the GNU General Public License v3.0

Copyright (C) 2016 Ben Hur S. Pintor (bhs.pintor@gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-------
"""

'''
dcc_constants.py 
CONSTANT VALUES, Styles, etc
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"

import sys

sys.dont_write_bytecode = True

try:
    import ttk
except ImportError:
    '''keep for Python 3 support'''
    import tkinter.ttk as ttk

# FONTS
RB_FONT = ('Times New Roman', 12)
BANNER_FONT = ('Times New Roman', 16)
LABEL_FONT = ('Arial', 10)
ENTRY_FONT = ('Arial', 10)
TOOLTIP_FONT = ('Arial', 9)

WIDTH = 480
HEIGHT = 480

# TOOLTIPS
'''Download'''
YEAR_TT = ("Enter the YEAR from which\n" +
    "the sensor data will be downloaded.")
MONTH_TT = ("Enter the MONTH (01-12) from which\n" +
    "the sensor data will be downloaded")
DAY_TT = ("Enter the DAY (01-31) of the month from whinh\n" +
    "the sensor data will be downloaded")
SENSOR_TT = ("Name of the SENSOR to be downloaded.\n" +
    "Leave blank for ALL sensors.\n" +
    "SENSORS WITH SOLAR RADIATION MEASURMENTS:\n" +
    "\t> BSWM_LUFFT\n" +
    "\t> -FIELD")
PROXY_TT = ("Enter the proxy server (if any)")
PORT_TT = ("Enter the proxy port (if any)")
DLSAVE_TT = ("Select the directory to save the downloaded sensor readings to.")

'''Compile'''
DLDIR_TT = ("The directory where the daily measurements csv's are located")
COMPFILE_TT = ("The file to save/append the monthly average values.")
SENTYPE_TT = ("The sensor type of the daily measurements to be compiled.")

COMPFILE2_TT = ("The input csv of compiled monthly average" + 
    " values per sensor and year.\n" +
    "(output of COMPILE PART 01)")
COMPILED_TT = ("The output csv of compiled monthly average values per sensor.")

'''Convert'''
INCSV_TT = ("The input csv of compiled monthly average values per sensor.")
OUTSHP_TT = ("The shapefile to be created.")


# COLORS
BG = '#333333'
BG_LIGHT = '#222222'
BG_DARK = '#444444'
FG = '#000000'
SEL = '#94A7C0'
SEL_DARK = '#657182'
FG_NB = '#F2F1F0'
