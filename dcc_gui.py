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
dcc_gui.py 
handles the GUI of the Tool
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"

import os
import sys

sys.dont_write_bytecode = True

try:
    import Tkinter as tk
    import ttk
    from Tkconstants import *
    import tkFileDialog as filedialog

except ImportError:
    '''keep for Python 3 support'''
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.constants import *
    import tkinter.filedialog as filedialog
    # print ("Tkinter not found. ")

import dcc_constants as con
import dcc_download
import dcc_compile
import dcc_convert


rb_font = con.RB_FONT
banner_font = con.BANNER_FONT
label_font = con.LABEL_FONT
entry_font = con.ENTRY_FONT
tt_font = con.TOOLTIP_FONT

width = con.WIDTH
height = con.HEIGHT

class ToolTip(object):
    """
    A class that creates a tooltip for a given widget when the mouse hovers
    over the widget.
    """

    def __init__(self, widget, tip="INFO"):
        """Initializes the tooltip.
        :param widget: the widget to attach the tooltip to
        :param tip: the tooltip string
        """

        self.widget = widget
        self.tip = tip
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.close)

    def enter(self, event=None):
        """Handles what happens when the mouse is over the widget"""
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Create a Toplevel window
        self.top = tk.Toplevel(self.widget)

        # Removes the app window of the Toplevel window
        self.top.wm_overrideredirect(True)
        self.top.wm_geometry('+%d+%d' %(x, y))
        label = tk.Label(self.top, text=self.tip, justify='left', background='#87CEFA',
                         relief='solid', borderwidth=1, font=tt_font)
        label.pack(ipadx=1)

    def close(self, event=None):
        """Handles what happens when the mouse leaves the widget"""
        if self.top:
            self.top.destroy()


class DownloadApp(tk.Frame):
    """A class for the Download Tool GUI"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=width, height=height)
        self.grid(sticky=N+E+W+S)

        '''Variables'''
        self.saveDirVar = tk.StringVar()
        self.saveDirVar.set(os.getcwd())

        '''Widgets'''
        self.headMast = tk.Label(self,
                                 text='Download ASTI Sensor Data',
                                 width=48,
                                 relief=RIDGE,
                                 borderwidth=2,
                                 background='yellow',
                                 font=banner_font)
        self.headMast.grid(row=0, sticky=N+E+W+S)

        #INPUTS
        self.inputsFrame = tk.Frame(self,
                                    relief=RIDGE,
                                    borderwidth=2,
                                    width=width-2,
                                    padx=1)
        self.inputsFrame.grid(row=1, sticky=N+E+W+S)

        self.yearLabel = tk.Label(self.inputsFrame,
                                  text='YEAR',
                                  relief=GROOVE,
                                  width=9,
                                  pady=2,
                                  padx=1,
                                  font=label_font)
        self.yearLabel.grid(row=0, column=0, sticky=E+W)
        self.yearEntry = tk.Entry(self.inputsFrame,
                                  width=12,
                                  font=entry_font)
        self.yearEntry.grid(row=0, column=1, sticky=E+W)
        self.yearTT = ToolTip(self.yearEntry,
                              con.YEAR_TT)

        self.monthLabel = tk.Label(self.inputsFrame,
                                   text='MONTH',
                                   relief=GROOVE,
                                   width=9,
                                   pady=2,
                                   padx=1,
                                   font=label_font)
        self.monthLabel.grid(row=0, column=2, sticky=E+W)
        self.monthEntry = tk.Entry(self.inputsFrame,
                                   width=12,
                                   font=entry_font)
        self.monthEntry.grid(row=0, column=3, sticky=E+W)
        self.monthTT = ToolTip(self.monthEntry,
                               con.MONTH_TT)

        self.dayLabel = tk.Label(self.inputsFrame,
                                 text='DAY',
                                 relief=GROOVE,
                                 width=9,
                                 pady=2,
                                 padx=1,
                                 font=label_font)
        self.dayLabel.grid(row=0, column=4, sticky=E+W)
        self.dayEntry = tk.Entry(self.inputsFrame,
                                 width=12,
                                 font=entry_font)
        self.dayEntry.grid(row=0, column=5, sticky=E+W)
        self.dayTT = ToolTip(self.dayEntry,
                             con.DAY_TT)

        self.sensorLabel = tk.Label(self.inputsFrame,
                                    text='KEYWORDS',
                                    relief=GROOVE,
                                    width=21,
                                    pady=2,
                                    padx=1,
                                    font=label_font)
        self.sensorLabel.grid(row=1, column=0, columnspan=2, sticky=E+W)
        self.sensorEntry = tk.Entry(self.inputsFrame,
                                    width=42,
                                    font=entry_font)
        self.sensorEntry.grid(row=1, column=2, columnspan=4, sticky=E+W)
        self.sensorTT = ToolTip(self.sensorEntry,
                                con.SENSOR_TT)

        # DOWNLOAD OPTIONS
        self.dlFrame = tk.Frame(self,
                                relief=RIDGE,
                                borderwidth=2,
                                width=width-2,
                                padx=1)
        self.dlFrame.grid(row=2, column=0, sticky=E+W)

        self.downloadOptionsLabel = tk.Label(self.dlFrame,
                                             anchor=W,
                                             font=rb_font)
        self.downloadOptionsLabel.grid(row=0, column=0, columnspan=5, sticky=E+W)

        self.proxyLabel = tk.Label(self.dlFrame,
                                   text='Proxy',
                                   relief=GROOVE,
                                   width=14,
                                   pady=2,
                                   padx=2,
                                   font=label_font)
        self.proxyLabel.grid(row=1, column=0, sticky=E+W)
        self.proxyEntry = tk.Entry(self.dlFrame,
                                   width=33,
                                   font=entry_font)
        self.proxyEntry.grid(row=1, column=1, columnspan=2, sticky=E+W)
        self.proxyTT = ToolTip(self.proxyEntry,
                               con.PROXY_TT)

        self.portLabel = tk.Label(self.dlFrame,
                                  text='Port',
                                  relief=GROOVE,
                                  width=9,
                                  pady=2,
                                  padx=2,
                                  font=label_font)
        self.portLabel.grid(row=1, column=3, sticky=E+W)
        self.portEntry = tk.Entry(self.dlFrame,
                                  width=8,
                                  font=entry_font)
        self.portEntry.grid(row=1, column=4, columnspan=2, sticky=E+W)
        self.portTT = ToolTip(self.portEntry,
                              con.PORT_TT)

        self.saveFileBtn = tk.Button(self.dlFrame,
                                     text="Save Folder",
                                     command=self.select_save,
                                     width=14,
                                     pady=2,
                                     padx=2,
                                     font=label_font)
        self.saveFileBtn.grid(row=2, column=0, sticky=E+W)
        self.saveDir = tk.Entry(self.dlFrame,
                                textvariable=self.saveDirVar,
                                readonlybackground='white',
                                state='readonly',
                                width=51,
                                font=entry_font)
        self.saveDir.grid(row=2, column=1, columnspan=4, sticky=E+W)
        self.saveDirTT = ToolTip(self.saveFileBtn,
                                 con.DLSAVE_TT)

        self.downloadBtn = tk.Button(self.dlFrame,
                                     text="DOWNLOAD SENSOR DATA",
                                     command=self.download_sensor,
                                     width=26,
                                     height=1,
                                     font=rb_font,
                                     activebackground='yellow')
        self.downloadBtn.grid(row=3, column=0, columnspan=2, sticky=E+W)


    def select_save(self):
        save = filedialog.askdirectory(parent=self,
                                       title='Select save file for ASTI sensor measurements')
        if save is None:
            self.saveDirVar.set(os.getcwd())
        else:
            self.saveDirVar.set(save)

    def download_sensor(self):
        proxy = self.proxyEntry.get().strip()
        port = self.portEntry.get().strip()
        saveDir = self.saveDirVar.get().strip()
        inputs = {'year': self.yearEntry.get().strip(), 
                  'month': self.monthEntry.get().strip(),
                  'day': self.dayEntry.get().strip(),
                  'sensor': self.sensorEntry.get().strip()}

        if proxy == "":
            os.chdir(saveDir)
            dcc_download.download_data(inputs)
            print "DONE!"
        
        else:
            PROXIES = {"http": "%s:%s" %(proxy, port)}
            os.chdir(saveDir)
            dcc_download.download_data(inputs, PROXIES)
            print "DONE!"


class CompileApp(tk.Frame):
    """A class for the Compile Tool GUI"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=width, height=height)
        self.grid()

        '''Variables'''
        self.dirVar = tk.StringVar()
        self.dirVar.set('')
        self.saveModeVar = tk.StringVar()
        self.saveModeVar.set('w')
        self.savePathVar = tk.StringVar()
        self.savePathVar.set('')
        self.optVar = tk.StringVar()
        self.optVar.set("BSWM_LUFFT")
        self.inputcsvVar = tk.StringVar()
        self.inputcsvVar.set('')
        self.outputcsvVar = tk.StringVar()
        self.outputcsvVar.set('')

        '''Widgets'''
        self.headMast1 = tk.Label(self,
                                  text='Compile ASTI Sensor Data PART 01',
                                  width=42,
                                  relief=RIDGE,
                                  borderwidth=2,
                                  background='yellow',
                                  font=banner_font)
        self.headMast1.grid(row=0, sticky=N+E+W)

        #INPUTS
        self.inputsFrame = tk.Frame(self,
                                    relief=RIDGE,
                                    borderwidth=2,
                                    width=width-2,
                                    padx=1)
        self.inputsFrame.grid(sticky=N+E+W+S)

        self.dirBtn = tk.Button(self.inputsFrame,
                                text="Select Directory",
                                command=self.select_dir,
                                width=14,
                                pady=2,
                                padx=1,
                                font=label_font)
        self.dirBtn.grid(row=0, sticky=E+W)
        self.dir = tk.Entry(self.inputsFrame,
                            textvariable=self.dirVar,
                            readonlybackground='white',
                            state='readonly',
                            width=52,
                            font=entry_font)
        self.dir.grid(row=0, column=1, columnspan=3, sticky=E+W)
        self.dirTT = ToolTip(self.dirBtn,
                             con.DLDIR_TT)

        self.saveFileBtn = tk.Button(self.inputsFrame,
                                     text="Save File",
                                     command=self.select_file,
                                     width=14,
                                     pady=2,
                                     padx=2,
                                     font=label_font)
        self.saveFileBtn.grid(row=2, column=0, sticky=E+W)
        self.savePath = tk.Entry(self.inputsFrame,
                                 textvariable=self.savePathVar,
                                 readonlybackground='white',
                                 state='readonly',
                                 width=50,
                                 font=entry_font)
        self.savePath.grid(row=2, column=1, columnspan=3, sticky=E+W)
        self.savePathTT = ToolTip(self.saveFileBtn,
                                  con.COMPFILE_TT)

        self.optLabel = tk.Label(self.inputsFrame,
                                 text='Sensor Type',
                                 relief=GROOVE,
                                 width=1,
                                 pady=2,
                                 padx=2,
                                 font=label_font)
        self.optLabel.grid(row=3, column=0, columnspan=1, sticky=E+W)
        self.optLabelTT = ToolTip(self.optLabel,
                                  con.SENTYPE_TT)

        self.optionMenu = tk.OptionMenu(self.inputsFrame,
                                        self.optVar,
                                        "BSWM_LUFFT", "FIELD")
        self.optionMenu.grid(row=3, column=1, columnspan=3, sticky=E+W)

        self.compileBtn = tk.Button(self.inputsFrame,
                                    text="COMPILE (MONTHLY AVERAGE PER SENSOR PER YEAR)",
                                    command=self.compile_measurements,
                                    width=36,
                                    height=1,
                                    font=rb_font,
                                    activebackground='yellow')
        self.compileBtn.grid(row=4, column=0, columnspan=4, sticky=E+W)

        self.headMast0 = tk.Label(self,
                                  width=42,
                                  relief=RIDGE,
                                  borderwidth=2,
                                  font=banner_font)
        self.headMast0.grid(row=2, sticky=N+E+W)

        # PART 02
        self.headMast2 = tk.Label(self,
                                  text='Compile ASTI Sensor Data PART 02',
                                  width=42,
                                  relief=RIDGE,
                                  borderwidth=2,
                                  background='yellow',
                                  font=banner_font)
        self.headMast2.grid(row=3, sticky=N+E+W)

        self.inputsFrame2 = tk.Frame(self,
                                     relief=RIDGE,
                                     borderwidth=2,
                                     width=width-2,
                                     padx=1)
        self.inputsFrame2.grid(sticky=N+E+W+S)

        self.inputcsvBtn = tk.Button(self.inputsFrame2,
                                     text="Input csv",
                                     command=self.select_inputcsv,
                                     width=14,
                                     pady=2,
                                     padx=1,
                                     font=label_font)
        self.inputcsvBtn.grid(row=0, sticky=E+W)
        self.inputcsvTT = ToolTip(self.inputcsvBtn,
                                  con.COMPFILE2_TT)

        self.inputcsvFile = tk.Entry(self.inputsFrame2,
                                     textvariable=self.inputcsvVar,
                                     readonlybackground='white',
                                     state='readonly',
                                     width=52,
                                     font=entry_font)
        self.inputcsvFile.grid(row=0, column=1, columnspan=3, sticky=E+W)

        self.outputcsvBtn = tk.Button(self.inputsFrame2,
                                      text="Output csv",
                                      command=self.select_outputcsv,
                                      width=14,
                                      pady=2,
                                      padx=1,
                                      font=label_font)
        self.outputcsvBtn.grid(row=1, sticky=E+W)
        self.outputcsvTT = ToolTip(self.outputcsvBtn,
                                   con.COMPILED_TT)

        self.outputcsvFile = tk.Entry(self.inputsFrame2,
                                      textvariable=self.outputcsvVar,
                                      readonlybackground='white',
                                      state='readonly',
                                      width=52,
                                      font=entry_font)
        self.outputcsvFile.grid(row=1, column=1, columnspan=3, sticky=E+W)

        self.compileBtn2 = tk.Button(self.inputsFrame2,
                                     text="COMPILE (MONTHLY AVERAGE PER SENSOR)",
                                     command=self.compile_persensor,
                                     width=36,
                                     height=1,
                                     font=rb_font,
                                     activebackground='yellow')
        self.compileBtn2.grid(row=2, column=0, columnspan=4, sticky=E+W)


    def select_dir(self):
        save = filedialog.askdirectory(parent=self,
                                       title="Select directory of daily solar measurements")
        if save is None:
            self.dirVar.set('')
        else:
            self.dirVar.set(save)

    def select_file(self):
        save = filedialog.asksaveasfilename(parent=self,
                                            filetypes=[('CSV', '.csv')],
                                            title='Select save file for compiled monthly average solar measurements')
        if save is None:
            self.savePathVar.set('')
        else:
            self.savePathVar.set(save)

    def select_inputcsv(self):
        save = filedialog.askopenfilename(parent=self,
                                          filetypes=[('CSV', '.csv')],
                                          title="Select CSV of monthly averages per year")
        if save is None:
            self.inputcsvVar.set('')
        else:
            self.inputcsvVar.set(save)

    def select_outputcsv(self):
        save = filedialog.asksaveasfilename(parent=self,
                                            filetypes=[('CSV', '.csv')],
                                            title='Select save file for monthly average solar measurements per sensor')
        if save is None:
            self.outputcsvVar.set('')
        else:
            self.outputcsvVar.set(save)


    def compile_measurements(self):

        directory = self.dirVar.get()
        saveMode = self.saveModeVar.get()
        savePath = self.savePathVar.get()
        opt = self.optVar.get()
        se = 0
        if opt == "BSWM_LUFFT":
            se = 7
        elif opt == "FIELD":
            se = 8

        dcc_compile.compile_data(directory, saveMode, savePath, se)

    def compile_persensor(self):

        inputcsv = self.inputcsvVar.get()
        outputcsv = self.outputcsvVar.get()

        dcc_compile.compile_to_csv(inputcsv, outputcsv)


class ConvertApp(tk.Frame):
    """A class for the Convert Tool GUI"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=width, height=height)
        self.grid()

        '''Variables'''
        self.incsvVar = tk.StringVar()
        self.incsvVar.set("")
        self.outshpVar = tk.StringVar()
        self.outshpVar.set("")

        '''Widgets'''
        self.headMast1 = tk.Label(self,
                                  text='Convert monthly average csv to shapefile',
                                  width=48,
                                  relief=RIDGE,
                                  borderwidth=2,
                                  background='yellow',
                                  font=banner_font)
        self.headMast1.grid(row=0, sticky=N+E+W)

        self.inputsFrame1 = tk.Frame(self,
                                     relief=RIDGE,
                                     borderwidth=2,
                                     width=width-2,
                                     padx=1)
        self.inputsFrame1.grid(sticky=N+E+W+S)

        self.incsvBtn = tk.Button(self.inputsFrame1,
                                     text="Input csv",
                                     command=self.select_incsv,
                                     width=14,
                                     pady=2,
                                     padx=1,
                                     font=label_font)
        self.incsvBtn.grid(row=0, sticky=E+W)
        self.incsvTT = ToolTip(self.incsvBtn,
                                  con.INCSV_TT)

        self.incsvFile = tk.Entry(self.inputsFrame1,
                                     textvariable=self.incsvVar,
                                     readonlybackground='white',
                                     state='readonly',
                                     width=52,
                                     font=entry_font)
        self.incsvFile.grid(row=0, column=1, columnspan=3, sticky=E+W)

        self.outshpBtn = tk.Button(self.inputsFrame1,
                                      text="Output shp",
                                      command=self.select_outshp,
                                      width=14,
                                      pady=2,
                                      padx=1,
                                      font=label_font)
        self.outshpBtn.grid(row=1, sticky=E+W)
        self.outshpvTT = ToolTip(self.outshpBtn,
                                   con.OUTSHP_TT)

        self.outshpFile = tk.Entry(self.inputsFrame1,
                                      textvariable=self.outshpVar,
                                      readonlybackground='white',
                                      state='readonly',
                                      width=52,
                                      font=entry_font)
        self.outshpFile.grid(row=1, column=1, columnspan=3, sticky=E+W)

        self.convertBtn = tk.Button(self.inputsFrame1,
                                    text="CONVERT CSV TO SHP",
                                    command=self.convert_csv_to_shp,
                                    width=36,
                                    height=1,
                                    font=rb_font,
                                    activebackground='yellow')
        self.convertBtn.grid(row=2, column=0, columnspan=4, sticky=E+W)


    def select_incsv(self):
        save = filedialog.askopenfilename(parent=self,
                                          filetypes=[('CSV', '.csv')],
                                          title="Select CSV of monthly averages per year")
        if save is None:
            self.incsvVar.set('')
        else:
            self.incsvVar.set(save)


    def select_outshp(self):
        save = filedialog.asksaveasfilename(parent=self,
                                            filetypes=[('SHP', '.shp')],
                                            title='Select save file for monthly average solar measurements per sensor')
        if save is None:
            self.outshpVar.set('')
        else:
            self.outshpVar.set(save)

    def convert_csv_to_shp(self):

        incsv = self.incsvVar.get()
        outshp = self.outshpVar.get()

        dcc_convert.csv_to_shp(incsv, outshp)