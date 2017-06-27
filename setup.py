# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 12:20:52 2017

@author: Malhotra
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Project_hdf5-GUI_version2.2",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Project_hdf5-GUI_version_2.2_working.py", base=base)])