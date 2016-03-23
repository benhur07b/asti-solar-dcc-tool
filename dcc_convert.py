#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
ASTI SOLAR RADIATION DATA DOWNLOAD, COMPILE, AND CONVERT TOOL

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
"""

'''
dcc_convert.py
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"

import shapefile
import pandas as pd

EPSG4326 = """GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""


def make_prj(inputshp, epsg):

    name = inputshp.split('.')[0] + ".prj"
    with open(name, "w") as prj:
        prj.write(epsg)

    print ".prj file created"


def csv_to_shp(inputcsv, outputshp):

    w = shapefile.Writer(shapefile.POINT)   # Create a POINT shapefile writer

    w.autoBalance = 1       # Enforce that every record must have a corresponding geometry

    # '''Create field names and data types'''
    # w.field("REGION", "C", "40")
    # w.field("PROVINCE", "C", "40")
    # w.field("LOCATION", "C", "40")
    # w.field("SENSOR_NAME", "C", "40")
    # w.field("JAN", "F")
    # w.field("FEB", "F")
    # w.field("MAR", "F")
    # w.field("APR", "F")
    # w.field("MAY", "F")
    # w.field("JUN", "F")
    # w.field("JUL", "F")
    # w.field("AUG", "F")
    # w.field("SEP", "F")
    # w.field("OCT", "F")
    # w.field("NOV", "F")
    # w.field("DEC", "F")

    df = pd.read_csv(inputcsv)      # Read the csv as a pandas dataframe
    headers = list(df)
    string_h = headers[2:6]
    float_h = headers[6:]

    '''Create field names and data types'''
    for h in string_h:
        w.field(h, "C", 40)

    for h in float_h:
        w.field(h, "F")

    for n in range(len(df)):        # Get the values per row
        lon = df.loc[n]['Longitude']
        lat = df.loc[n]['Latitude']
        reg = df.loc[n]['Region']
        pro = df.loc[n]['Province']
        loc = df.loc[n]['Location']
        sen = df.loc[n]['Sensor_Name']
        jan = df.loc[n]['JAN']
        feb = df.loc[n]['FEB']
        mar = df.loc[n]['MAR']
        apr = df.loc[n]['APR']
        may = df.loc[n]['MAY']
        jun = df.loc[n]['JUN']
        jul = df.loc[n]['JUL']
        aug = df.loc[n]['AUG']
        sep = df.loc[n]['SEP']
        ocr = df.loc[n]['OCT']
        nov = df.loc[n]['NOV']
        dec = df.loc[n]['DEC']

        w.point(lon, lat)   # Add geometry

        w.record(reg, pro, loc, sen, jan, feb, mar, apr, may, jun, jul, aug, sep, ocr, nov, dec)    # Update records


        print "Feature %i added to Shapefile" %(n+1)

    w.save(outputshp)

    make_prj(outputshp, EPSG4326)