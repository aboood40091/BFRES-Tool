#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Copyright © 2017 AboodXD

# This file is part of BFRES Tool.

# BFRES Tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# BFRES Tool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""build.py: Build an executable for BFRES Tool."""

import os, shutil, sys
from cx_Freeze import setup, Executable

version = '0.1'

# Pick a build directory
dir_ = 'bfres_tool v' + version

# Add the "build" parameter to the system argument list
if 'build' not in sys.argv:
    sys.argv.append('build')

# Clear the directory
print('>> Clearing/creating directory...')
if os.path.isdir(dir_): shutil.rmtree(dir_)
os.makedirs(dir_)
print('>> Directory ready!')

setup(
    name = 'BFRES Tool',
    version = version,
    description = 'Wii U BFRES Tool',
    author = "AboodXD",
    options={
        'build_exe': {
            'compressed': 1,
            'build_exe': dir_,
            },
        },
    executables = [
        Executable(
            'bfres_tool.py',
            ),
        ],
    )

print('>> Attempting to copy required files...')
shutil.copy('COPYING', dir_)
shutil.copy('DDStoGTX.bat', dir_)
shutil.copy('GTXtoDDS.bat', dir_)
shutil.copy('tileMode.txt', dir_)
print('>> Files copied!')

print('>> BFRES Tool has been frozen to "%s"!' % dir_)
