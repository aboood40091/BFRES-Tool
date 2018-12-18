#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Version 5.0
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

Version = '5.0'

formats = {
    0x00000001: 'GX2_SURFACE_FORMAT_TC_R8_UNORM',
    0x00000002: 'GX2_SURFACE_FORMAT_TC_R4_G4_UNORM',
    0x00000007: 'GX2_SURFACE_FORMAT_TC_R8_G8_UNORM',
    0x00000008: 'GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM',
    0x0000000a: 'GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM',
    0x0000000b: 'GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM',
    0x00000019: 'GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM',
    0x0000001a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM',
    0x0000041a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB',
    0x00000031: 'GX2_SURFACE_FORMAT_T_BC1_UNORM',
    0x00000431: 'GX2_SURFACE_FORMAT_T_BC1_SRGB',
    0x00000032: 'GX2_SURFACE_FORMAT_T_BC2_UNORM',
    0x00000432: 'GX2_SURFACE_FORMAT_T_BC2_SRGB',
    0x00000033: 'GX2_SURFACE_FORMAT_T_BC3_UNORM',
    0x00000433: 'GX2_SURFACE_FORMAT_T_BC3_SRGB',
    0x00000034: 'GX2_SURFACE_FORMAT_T_BC4_UNORM',
    0x00000234: 'GX2_SURFACE_FORMAT_T_BC4_SNORM',
    0x00000035: 'GX2_SURFACE_FORMAT_T_BC5_UNORM',
    0x00000235: 'GX2_SURFACE_FORMAT_T_BC5_SNORM',
}

formats2 = {
    0x00000001: 'L8',
    0x00000002: 'L4A4 / LA4',
    0x00000007: 'L8A8 / LA8',
    0x00000008: 'R5G6B5 / RGB565',
    0x0000000a: 'A1RGB5 / A1BGR5',
    0x0000000b: 'ARGB4 / ABGR4',
    0x00000019: 'A2RGB10 / A2BGR10',
    0x0000001a: 'ARGB8 / ABGR8',
    0x0000041a: 'ARGB8 / ABGR8',
    0x00000031: 'BC1 / DXT1',
    0x00000431: 'BC1 / DXT1',
    0x00000032: 'BC2 / DXT3',
    0x00000432: 'BC2 / DXT3',
    0x00000033: 'BC3 / DXT5',
    0x00000433: 'BC3 / DXT5',
    0x00000034: 'BC4U / ATI1',
    0x00000234: 'BC4S / ATI1',
    0x00000035: 'BC5U / ATI2',
    0x00000235: 'BC5S / ATI2',
}

tileModes = {
    0x00: 'GX2_TILE_MODE_DEFAULT',
    0x01: 'GX2_TILE_MODE_LINEAR_ALIGNED',
    0x02: 'GX2_TILE_MODE_1D_TILED_THIN1',
    0x03: 'GX2_TILE_MODE_1D_TILED_THICK',
    0x04: 'GX2_TILE_MODE_2D_TILED_THIN1',
    0x05: 'GX2_TILE_MODE_2D_TILED_THIN2',
    0x06: 'GX2_TILE_MODE_2D_TILED_THIN4',
    0x07: 'GX2_TILE_MODE_2D_TILED_THICK',
    0x08: 'GX2_TILE_MODE_2B_TILED_THIN1',
    0x09: 'GX2_TILE_MODE_2B_TILED_THIN2',
    0x0a: 'GX2_TILE_MODE_2B_TILED_THIN4',
    0x0b: 'GX2_TILE_MODE_2B_TILED_THICK',
    0x0c: 'GX2_TILE_MODE_3D_TILED_THIN1',
    0x0d: 'GX2_TILE_MODE_3D_TILED_THICK',
    0x0e: 'GX2_TILE_MODE_3B_TILED_THIN1',
    0x0f: 'GX2_TILE_MODE_3B_TILED_THICK',
    0x10: 'GX2_TILE_MODE_LINEAR_SPECIAL',
}

compSels = {
    0: "Red", 1: "Green",
    2: "Blue", 3: "Alpha",
    4: "0", 5: "1",
}

BCn_formats = [
    0x31, 0x431, 0x32, 0x432,
    0x33, 0x433, 0x34, 0x234,
    0x35, 0x235,
]


fileData = bytearray()
texSizes = []
