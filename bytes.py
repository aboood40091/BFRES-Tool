#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Version 5.1
# Copyright © 2017-2018 AboodXD

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

def bytes_to_string(data, pos=0, end=0):
    if not end:
        end = data.find(b'\0', pos)
        if end == -1:
            return data[pos:].decode('utf-8')

    return data[pos:end].decode('utf-8')
