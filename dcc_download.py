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

INSTRUCTIONS FOR RUNNING
1. Open terminal (CTRL+ALT+T in Ubuntu).
2. Go to asti-solar-dcc-tool directory.
3. Type python dcc.py

N.B.
Make sure that the modules found in requirements.txt are installed/present
in the computer.
If not, try installing them by typing on your terminal:
    pip install -r requirements.text

"""

'''
dcc_download.py
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"

from bs4 import BeautifulSoup
import requests
import shutil
import re
import sys
from datetime import datetime

sys.dont_write_bytecode = True

ASTI_URL = "http://repo.pscigrid.gov.ph/predict"


def get_links(r):

    links = list()
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return links


def save_to_file(url, name, proxies):

    r = requests.get(url, stream=True, proxies=proxies)
    with open(name, 'wb') as outfile:
        shutil.copyfileobj(r.raw, outfile)
    del r
    print "%s: Saved to file" %name


def scrape_data(url0, start, dataset, proxies):

    for data in range(start, len(dataset)):
        url = url0 + "/%s" %dataset[data]
        save_to_file(url, dataset[data], proxies)


def scrape_day_asti(y, m, d, proxies):
    """Scrapes data from all the sensors for a specific day."""

    url = ASTI_URL + "/%s/%s/%s" %(y, m, d)
    r = requests.get(url, proxies=proxies)
    sensors = get_links(r)
    scrape_data(url, 1, sensors, proxies)


def scrape_month_asti(y, m, proxies):
    """Scrapes data from all the sensors for a specific month."""

    url = ASTI_URL + "/%s/%s" %(y, m)
    r = requests.get(url, proxies=proxies)
    days = get_links(r)
    for d in range(1, len(days)):
        scrape_day_asti(y, m, days[d], proxies)


def scrape_year_asti(y, proxies):
    """Scrapes data from all the sensors for a specific year."""

    url = ASTI_URL + "/%s" %(y)
    r = requests.get(url, proxies=proxies)
    months = get_links(r)
    for m in range(1, len(months)):
        scrape_month_asti(y, months[m], proxies)


def get_sensors(r, sensor):

    links = list()
    soup = BeautifulSoup(r.text)
    for link in soup.find_all(href=re.compile(sensor)):
        links.append(link.get('href'))

    return links


def scrape_day_sensor(y, m, d, sensor, proxies):
    """Scrapes data from all the sensors for a specific day."""

    url = ASTI_URL + "/%s/%s/%s" %(y, m, d)
    r = requests.get(url, proxies=proxies)
    sensors = get_sensors(r, sensor)
    scrape_data(url, 1, sensors, proxies)


def scrape_month_sensor(y, m, sensor, proxies):
    """Scrapes data from all the sensors for a specific month."""

    url = ASTI_URL + "/%s/%s" %(y, m)
    r = requests.get(url, proxies=proxies)
    days = get_links(r)
    for d in range(1, len(days)):
        scrape_day_sensor(y, m, days[d], sensor, proxies)


def scrape_year_sensor(y, sensor, proxies):
    """Scrapes data from all the sensors for a specific year."""

    url = ASTI_URL + "/%s" %(y)
    r = requests.get(url, proxies=proxies)
    months = get_links(r)
    for m in range(1, len(months)):
        scrape_month_asti(y, months[m], sensor, proxies)


def download_data(inputs, proxies):

    y = inputs['year']
    m = inputs['month']
    d = inputs['day']
    s = inputs['sensor']

    try:
        if y != '' and m != '' and d != '':
            if datetime(int(y), int(m), int(d)):
                if s == '':
                    scrape_day_asti(y, m, d, proxies)
                else:
                    scrape_day_sensor(y, m, d, s, proxies)

        if y != '' and m != '' and d == '':
            if datetime(int(y), int(m), 1):
                if s == '':
                    scrape_month_asti(y, m, proxies)
                else:
                    scrape_month_sensor(y, m, s, proxies)

        if y != '' and m == '' and d == '':
            if datetime(int(y), 1, 1):
                if s == '':
                    scrape_year_asti(y, proxies)
                else:
                    scrape_year_sensor(y, s, proxies)

    except ValueError:
        print "Input Error."
