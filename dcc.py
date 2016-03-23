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
dcc.py 
the main app
'''

__author__ = "Ben Hur S. Pintor"
__contact__ = "bhs.pintor<at>gmail.com"
__version__ = "0.0.1"


try:
    import Tkinter as tk
    import ttk
    from Tkconstants import *
except ImportError:
    '''keep for Python 3 support'''
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.constants import *
    # print ("Tkinter not found. ")

import dcc_constants as con
import dcc_gui

def main():
    root = tk.Tk()
    root.title('ASTI Solar Download, Compile, and Convert Tool')
    icon = tk.Image('photo', file='imgs/Solar.png')
    root.tk.call('wm', 'iconphoto', root._w, icon)
    root.geometry('{}x{}'.format(con.WIDTH, con.HEIGHT))
    root.resizable(width=FALSE, height=FALSE)
    style = ttk.Style()
    style.configure(".",
                    background=con.BG_LIGHT,
                    fieldbackground=con.BG,
                    foreground=con.FG, 
                    )
    style.configure("TNotebook.Tab",
                    foreground=con.FG_NB, 
                    )
    style.map(".", background=[("active", con.BG_DARK)])
    style.map("TNotebook.Tab", background=[("selected", con.BG),
                                       ("!selected", con.BG_DARK)])

    # NOTEBOOK
    nb = ttk.Notebook(root,
                      height=con.HEIGHT-90,
                      width=con.WIDTH)

    dl = dcc_gui.DownloadApp(nb)
    cm = dcc_gui.CompileApp(nb)
    cn = dcc_gui.ConvertApp(nb)



    nb.add(dl, text="DOWNLOAD", sticky=E+W)
    nb.add(cm, text="COMPILE", sticky=E+W)
    nb.add(cn, text="CONVERT", sticky=E+W)

    nb.grid(row=0, column=0, sticky=N+E+W+S)


    # MENUBARS
    menubar = tk.Menu(root)
    aboutmenu = tk.Menu(menubar, tearoff=0)
    aboutmenu.add_command(label="README", command=show_readme)

    menubar.add_cascade(label='About', menu=aboutmenu)
    root.config(menu=menubar)

    decor = tk.Frame(root)
    decor.grid(row=1, column=0, sticky=N+E+W+S)
    logo = tk.Image('photo', file='imgs/Solar.png')
    logoLabel = tk.Label(decor,
                         height=64,
                         width=64,
                         relief=RAISED,
                         background='white',
                         image=logo)
    logoLabel.grid()


    root.mainloop()


def show_readme():
    top = tk.Toplevel()
    top.title("README")
    top.resizable(width=FALSE, height=FALSE)
    msg = tk.Message(top, text=__doc__)
    msg.pack()

# def show_about():
#     pass

# def show_solar():
#     pass


if __name__ == '__main__':
    main()
