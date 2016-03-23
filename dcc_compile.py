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
dcc_compile.py
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"


import os
import sys
import csv
import numpy as np
import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter

sys.dont_write_bytecode = True


def compile_data(directory, saveMode, savePath, se):

    flist = os.listdir(directory)   # get list of files
    sortedFiles = sorted(flist)     # sort list of files alphabetically

    groupedIter = groupby(sortedFiles, key=itemgetter(slice(None,-13)))     # readings grouped by name

    groupedList = [list(f[1]) for f in groupedIter]     # nested list of readings grouped by sensor


    if os.path.exists(savePath):
        o = open(savePath, 'a')

    else:
        o = open(savePath, 'w')
        o.write('region,province,location,posx,posy,elevation,sensor_name,year,month,solar radiation average (daily),days\n')

    dailyAves = []

    '''Set the time ranges.'''
    lowerTime = datetime.now().replace(hour=5, minute=0, second=0).time()
    upperTime = datetime.now().replace(hour=19, minute=0, second=0).time()
    lowerMidTime = datetime.now().replace(hour=9, minute=0, second=0).time()
    upperMidTime = datetime.now().replace(hour=15, minute=0, second=0).time()


    for group in groupedList:

        for f in group:
            headers = {}

            with open(os.path.join(directory, f)) as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                totalReadings = 0
                midDayReadings = 0
                noneReadings = 0
                readings = []
                times = []
                goodQuality = False

                for row in reader:
                    if len(row) < 3:            # heading lines < 3 rows
                        headers[row[0].split(':')[0]] = row[0].split(':')[1][1:]

                    headers['year'] = str(f[-12:-8])
                    headers['month'] = str(f[-8:-6])
                    headers['day'] = str(f[-6:-4])

                    if len(row) > 3 and row[0] != 'dateTimeRead(YYYY-MM-DD HH-mm-ss)':

                        readingTime = parser.parse(row[0])

                        if row[se] != 'None':
                            readings.append(float(row[se]))
                            times.append(readingTime)

                            if readingTime.time() >= lowerTime and readingTime.time() <= upperTime:
                                totalReadings += 1

                            if readingTime.time() >= lowerMidTime and readingTime.time() <= upperMidTime:
                                midDayReadings += 1
                
                if len(times) > 2:
                    timeDiffs = np.ediff1d(np.array(times))
                    positiveTimeDiffs = timeDiffs[timeDiffs > timedelta(0,61)]
                    i = int((np.amin(positiveTimeDiffs).seconds + 30)/60.0)

                    totalThreshold = int(14 * (60.0/i))
                    midDayThreshold = int(0.8 * (6 * (60.0/i)))


                    if totalReadings >= totalThreshold:
                        goodQuality = True

                    elif totalReadings in range(totalThreshold - int(2 * (60/i)), totalThreshold):
                        if midDayReadings >= midDayThreshold:
                            goodQuality = True

                        else:
                            goodQuality = False

                    else:
                        goodQuality = False

                    if goodQuality:
                        dailyAves.append(np.sum(np.array(readings))/(60.0/i))
                        print "Done with %s" %f
        
        if len(dailyAves) > 0:
            monthlyAve = np.mean(np.array(dailyAves))
            s = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%.4f,%i\n" %(headers['region'], headers['province'],
                                                         headers['location'], headers['posx'],
                                                         headers['posy'], headers['elevation'],
                                                         headers['sensor_name'], headers['year'],
                                                         headers['month'], monthlyAve, len(dailyAves))

            o.write(s)
        del dailyAves[:]

    print "Done with directory %s" %directory

    o.close()


def compile_to_csv(inputcsv, outputcsv):

    with open(outputcsv, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['Longitude', 'Latitude', 'Region', 'Province', 'Location', 'Sensor_Name', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL' , 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'])

        monthly_aves = []   # list of monthly averages for a sensor/location

        df = pd.read_csv(inputcsv)   # read the csv file of compiled monthly averages
        grouped_1 = df.groupby(['region', 'province', 'location'])  # group the monthly averages based on sensor/location
                                                                    # grouping will include monthly readings for each sensor/location

        for name1, group1 in grouped_1:
            del monthly_aves[:]          # make sure the list of monthly averages is empty
            lat = group1['posx'].max()          # get the posx of the sensor/location (Latitude)
            lon = group1['posy'].max()          # get the posy of the sensor/location (Longitude)
            reg = group1['region'].max()        # get the region of the sensor/location
            pro = group1['province'].max()      # get the province of the sensor/location
            loc = group1['location'].max()      # get the location of the sensor/location
            sen = group1['sensor_name'].max()   # get the sensor name of the sensor/location
            
            grouped_2 = group1.groupby('month')    # group the readings based on month

            for name2, group2 in grouped_2:
                monthly_ave = group2.groupby(group2.index).apply(lambda x: np.average(group2['solar radiation average (daily)'], weights=group2['days'])).max()
                monthly_aves.append(monthly_ave)

            if lat > 0 and lon > 0:     # if there are latlon values, add to shapefile
                writer.writerow([lon, lat, reg, pro, loc, sen] + monthly_aves)

            else:
                pass
