#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Version 3.1
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

"""bfres_tool.py: The main executable."""

import os, sys, struct, time
import requests
import shutil
from tkinter import Tk, Frame, Button, Canvas, Scrollbar, Menu
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
import urllib.request
import warnings

top = Tk()
canvas = Canvas(top)
frame = Frame(canvas)
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)

formats = {0x00000001: 'GX2_SURFACE_FORMAT_TC_R8_UNORM',
           0x00000002: 'GX2_SURFACE_FORMAT_TC_R4_G4_UNORM',
           0x00000007: 'GX2_SURFACE_FORMAT_TC_R8_G8_UNORM',
           0x00000008: 'GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM',
           0x0000000a: 'GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM',
           0x0000000b: 'GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM',
           0x0000000c: 'GX2_SURFACE_FORMAT_TC_A1_B5_G5_R5_UNORM',
           0x00000019: 'GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM',
           0x0000001a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM',
           0x0000041a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB',
           0x0000001b: 'GX2_SURFACE_FORMAT_TCS_A2_B10_G10_R10_UNORM',
           0x0000001f: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_UNORM',
           0x00000820: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_FLOAT',
           0x00000823: 'GX2_SURFACE_FORMAT_TC_R32_G32_B32_A32_FLOAT',
           0x00000031: 'GX2_SURFACE_FORMAT_T_BC1_UNORM',
           0x00000431: 'GX2_SURFACE_FORMAT_T_BC1_SRGB',
           0x00000032: 'GX2_SURFACE_FORMAT_T_BC2_UNORM',
           0x00000432: 'GX2_SURFACE_FORMAT_T_BC2_SRGB',
           0x00000033: 'GX2_SURFACE_FORMAT_T_BC3_UNORM',
           0x00000433: 'GX2_SURFACE_FORMAT_T_BC3_SRGB',
           0x00000034: 'GX2_SURFACE_FORMAT_T_BC4_UNORM',
           0x00000234: 'GX2_SURFACE_FORMAT_T_BC4_SNORM',
           0x00000035: 'GX2_SURFACE_FORMAT_T_BC5_UNORM',
           0x00000235: 'GX2_SURFACE_FORMAT_T_BC5_SNORM'
           }

BCn_formats = [0x31, 0x431, 0x32, 0x432, 0x33, 0x433, 0x34, 0x234, 0x35, 0x235]

supported_formats = {0x00000001: 'GX2_SURFACE_FORMAT_TC_R8_UNORM',
                     0x00000002: 'GX2_SURFACE_FORMAT_TC_R4_G4_UNORM',
                     0x00000007: 'GX2_SURFACE_FORMAT_TC_R8_G8_UNORM',
                     0x00000008: 'GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM',
                     0x0000000a: 'GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM',
                     0x0000000b: 'GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM',
                     0x0000000c: 'GX2_SURFACE_FORMAT_TC_A1_B5_G5_R5_UNORM',
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
                     0x00000235: 'GX2_SURFACE_FORMAT_T_BC5_SNORM'
                     }

tileModes = {0x00: 'GX2_TILE_MODE_DEFAULT',
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
             0x10: 'GX2_TILE_MODE_LINEAR_SPECIAL'}

formats2 = {0x00000001: 'L8',
            0x00000002: 'L4A4 / LA4',
            0x00000007: 'L8A8 / LA8',
            0x00000008: 'R5G6B5 / RGB565',
            0x0000000a: 'A1RGB5 / A1BGR5',
            0x0000000b: 'ARGB4 / ABGR4',
            0x0000000c: 'A1RGB5 / A1BGR5',
            0x00000019: 'A2RGB10 / A2BGR10',
            0x0000001a: 'ARGB8 / ABGR8',
            0x0000041a: 'ARGB8 / ABGR8',
            0x0000001b: 'A2RGB10 / A2BGR10',
            0x0000001f: 'RGBA16',
            0x00000820: 'RGBA16_FLOAT',
            0x00000823: 'RGBA32_FLOAT',
            0x00000031: 'BC1 / DXT1',
            0x00000431: 'BC1 / DXT1',
            0x00000032: 'BC2 / DXT3',
            0x00000432: 'BC2 / DXT3',
            0x00000033: 'BC3 / DXT5',
            0x00000433: 'BC3 / DXT5',
            0x00000034: 'BC4U / ATI1',
            0x00000234: 'BC4S / ATI1',
            0x00000035: 'BC5U / ATI2',
            0x00000235: 'BC5S / ATI2'
            }

class groups():
    pass

def find_name(f, name_pos):
    name = b""
    char = f[name_pos:name_pos + 1]
    i = 1

    while char != b"\x00":
        name += char
        
        char = f[name_pos + i:name_pos + i + 1]
        i += 1

    return(name.decode("utf-8"))

def FTEXtoDDS(ftex_pos, f, name, folder):
    ftex = f[ftex_pos:ftex_pos+0xC0]
    info = ftex[0x4:0x8C] + bytearray.fromhex("0000000000000000000000000000000000000000")

    format_ = struct.unpack(">I", info[0x14:0x18])[0]

    if format_ in formats:
        head1 = bytearray.fromhex("4766783200000020000000070000000100000002000000000000000000000000424C4B7B0000002000000001000000000000000B0000009C0000000000000000")
        head4 = bytearray.fromhex("424C4B7B00000020000000010000000000000001000000000000000000000000")

        dataSize = struct.unpack(">I", info[0x20:0x24])[0]
        mipSize = struct.unpack(">I", info[0x28:0x2C])[0]

        head2 = bytearray.fromhex("424C4B7B0000002000000001000000000000000C") + dataSize.to_bytes(4, 'big') + bytearray.fromhex("0000000000000000")

        data_pos = struct.unpack(">I", f[ftex_pos+0xB0:ftex_pos+0xB4])[0] + ftex_pos + 0xB0
        mip_pos = struct.unpack(">I", f[ftex_pos+0xB4:ftex_pos+0xB8])[0]

        data = f[data_pos:data_pos+dataSize]

        if mip_pos == 0:
            head3 = b""
            mip = b""
        else:
            mip_pos += ftex_pos + 0xB4
            head3 = bytearray.fromhex("424C4B7B0000002000000001000000000000000D") + mipSize.to_bytes(4, 'big') + bytearray.fromhex("0000000000000000")
            mip = f[mip_pos:mip_pos+mipSize]

        file = head1 + info + head2 + data + head3 + mip + head4

        with open(folder + "\\" + name + "2.gtx", "wb") as output:
            output.write(file)
            output.close()

        width = struct.unpack(">I", info[0x04:0x08])[0]
        height = struct.unpack(">I", info[0x08:0x0C])[0]
        depth = struct.unpack(">I", info[0x0C:0x10])[0]
        aa = struct.unpack(">I", info[0x18:0x1C])[0]

        print("")
        os.system('C:\Tex\TexConv2.exe -i "' + folder + "\\" + name + '2.gtx" -f GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM -o "' + folder + "\\" + name + '.gtx"')
        os.system('C:\Tex\gtx_extract.exe "' + folder + "\\" + name + '.gtx"')
        try:
            os.remove(folder + "\\" + name + '.gtx')
        except FileNotFoundError:
            os.system('C:\Tex\TexConv2.exe -i "' + folder + "\\" + name + '2.gtx" -o "' + folder + "\\" + name + '.dds"')

            if ((format_ in supported_formats) and (depth == 1) and (aa == 0)):
                if os.path.isfile(folder + "\\" + name + '.dds'):
                    if (format_ == 0x1a or format_ == 0x41a):
                        format__ = 28
                    elif format_ == 0x19:
                        format__ = 24
                    elif format_ == 0x8:
                        format__ = 85
                    elif format_ == 0xa:
                        format__ = 86
                    elif format_ == 0xb:
                        format__ = 115
                    elif format_ == 0x1:
                        format__ = 61
                    elif format_ == 0x7:
                        format__ = 49
                    elif format_ == 0x2:
                        format__ = 112
                    elif (format_ == 0x31 or format_ == 0x431):
                        format__ = "BC1"
                    elif (format_ == 0x32 or format_ == 0x432):
                        format__ = "BC2"
                    elif (format_ == 0x33 or format_ == 0x433):
                        format__ = "BC3"
                    elif format_ == 0x34:
                        format__ = "BC4U"
                    elif format_ == 0x234:
                        format__ = "BC4S"
                    elif format_ == 0x35:
                        format__ = "BC5U"
                    elif format_ == 0x235:
                        format__ = "BC5S"

                    hdr = writeHeader(1, width, height, format__, format_ in BCn_formats)

                    with open(folder + "\\" + name + ".dds", "rb") as output:
                        out = bytearray(output.read())
                        output.close()

                    with open(folder + "\\" + name + ".dds", "wb") as output:
                        out[:0x80] = hdr
                        output.write(out)
                        output.close()
                else:
                    format_ = 0

        os.remove(folder + "\\" + name + '2.gtx')

    return format_

# ----------\/-DDS writer-\/---------- #

# Copyright © 2016-2017 AboodXD

# Supported formats:
#  -RGBA8
#  -RGB10A2
#  -RGB565
#  -RGB5A1
#  -RGBA4
#  -L8
#  -L8A8
#  -L4A4
#  -BC1_UNORM
#  -BC2_UNORM
#  -BC3_UNORM
#  -BC4_UNORM
#  -BC4_SNORM
#  -BC5_UNORM
#  -BC5_SNORM

# Feel free to include this in your own program if you want, just give credits. :)

def writeHeader(num_mipmaps, w, h, format_, compressed):
    hdr = bytearray(128)

    if format_ == 28: # RGBA8
        fmtbpp = 4
        has_alpha = 1
        rmask = 0x000000ff
        gmask = 0x0000ff00
        bmask = 0x00ff0000
        amask = 0xff000000

    elif format_ == 24: # RGB10A2
        fmtbpp = 4
        has_alpha = 1
        rmask = 0x000003ff
        gmask = 0x000ffc00
        bmask = 0x3ff00000
        amask = 0xc0000000

    elif format_ == 85: # RGB565
        fmtbpp = 2
        has_alpha = 0
        rmask = 0x0000001f
        gmask = 0x000007e0
        bmask = 0x0000f800
        amask = 0x00000000

    elif format_ == 86: # RGB5A1
        fmtbpp = 2
        has_alpha = 1
        rmask = 0x0000001f
        gmask = 0x000003e0
        bmask = 0x00007c00
        amask = 0x00008000

    elif format_ == 115: # RGBA4
        fmtbpp = 2
        has_alpha = 1
        rmask = 0x0000000f
        gmask = 0x000000f0
        bmask = 0x00000f00
        amask = 0x0000f000

    elif format_ == 61: # L8
        fmtbpp = 1
        has_alpha = 0
        rmask = 0x000000ff
        gmask = 0x000000ff
        bmask = 0x000000ff
        amask = 0x00000000

    elif format_ == 49: # L8A8
        fmtbpp = 2
        has_alpha = 1
        rmask = 0x000000ff
        gmask = 0x000000ff
        bmask = 0x000000ff
        amask = 0x0000ff00

    elif format_ == 112: # L4A4
        fmtbpp = 1
        has_alpha = 1
        rmask = 0x0000000f
        gmask = 0x0000000f
        bmask = 0x0000000f
        amask = 0x000000f0

    flags = (0x00000001) | (0x00001000) | (0x00000004) | (0x00000002)

    caps = (0x00001000)

    if num_mipmaps == 0: num_mipmaps = 1
    if num_mipmaps != 1:
        flags |= (0x00020000)
        caps |= ((0x00000008) | (0x00400000))

    if not compressed:
        flags |= (0x00000008)

        if (fmtbpp == 1 or format_ == 49): # LUMINANCE
            pflags = (0x00020000)

        else: # RGB
            pflags = (0x00000040)

        if has_alpha != 0:
            pflags |= (0x00000001)

        size = w * fmtbpp

    else:
        flags |= (0x00080000)
        pflags = (0x00000004)

        if format_ == "BC1":
            fourcc = b'DXT1'
        elif format_ == "BC2":
            fourcc = b'DXT3'
        elif format_ == "BC3":
            fourcc = b'DXT5'
        elif format_ == "BC4U":
            fourcc = b'BC4U'
        elif format_ == "BC4S":
            fourcc = b'BC4S'
        elif format_ == "BC5U":
            fourcc = b'BC5U'
        elif format_ == "BC5S":
            fourcc = b'BC5S'

        size = ((w + 3) >> 2) * ((h + 3) >> 2)
        if (format_ == "BC1" or format_ == "BC4U" or format_ == "BC4S"):
            size *= 8
        else:
            size *= 16

    hdr[:4] = b'DDS '
    hdr[4:4+4] = 124 .to_bytes(4, 'little')
    hdr[8:8+4] = flags.to_bytes(4, 'little')
    hdr[12:12+4] = h.to_bytes(4, 'little')
    hdr[16:16+4] = w.to_bytes(4, 'little')
    hdr[20:20+4] = size.to_bytes(4, 'little')
    hdr[28:28+4] = num_mipmaps.to_bytes(4, 'little')
    hdr[76:76+4] = 32 .to_bytes(4, 'little')
    hdr[80:80+4] = pflags.to_bytes(4, 'little')

    if compressed:
        hdr[84:84+4] = fourcc
    else:
        hdr[88:88+4] = (fmtbpp << 3).to_bytes(4, 'little')
        hdr[92:92+4] = rmask.to_bytes(4, 'little')
        hdr[96:96+4] = gmask.to_bytes(4, 'little')
        hdr[100:100+4] = bmask.to_bytes(4, 'little')
        hdr[104:104+4] = amask.to_bytes(4, 'little')

    hdr[108:108+4] = caps.to_bytes(4, 'little')

    return hdr

def DDStoBFRES(ftex_pos, dds, bfres):
    with open(bfres, "rb") as inf:
        inb = inf.read()
        inf.close()

    name = os.path.splitext(dds)[0]

    os.system('C:\Tex\TexConv2.exe -i "' + dds + '" -o "' + name + '.gtx"')

    swizzle = struct.unpack(">I", inb[ftex_pos+0x38:ftex_pos+0x3C])[0]
    swizzle = (swizzle & 0xFFF) >> 8
    format_ = struct.unpack(">I", inb[ftex_pos+0x18:ftex_pos+0x1C])[0]
    tileMode = struct.unpack(">I", inb[ftex_pos+0x34:ftex_pos+0x38])[0]
    numMips = struct.unpack(">I", inb[ftex_pos+0x14:ftex_pos+0x18])[0]

    if numMips > 1:
        os.system('C:\Tex\TexConv2.exe -i "' + name + '.gtx" -f ' + formats[format_] + ' -tileMode ' + tileModes[tileMode] + ' -swizzle ' + str(swizzle) + ' -mipFilter box -minmip 1 -o "' + name + '2.gtx"')
    else:
        os.system('C:\Tex\TexConv2.exe -i "' + name + '.gtx" -f ' + formats[format_] + ' -tileMode ' + tileModes[tileMode] + ' -swizzle ' + str(swizzle) + ' -o "' + name + '2.gtx"')

    os.remove(name + '.gtx')

    with open(name + '2.gtx', "rb") as gfd1:
        gfd = gfd1.read()
        gfd1.close()

    if inb[:4] != b"FRES":
        messagebox.showinfo("", "Invalid BFRES header!")
        os.remove(name + '2.gtx')

    elif gfd[:4] != b"Gfx2":
        messagebox.showinfo("", "Invalid GTX header!")
        os.remove(name + '2.gtx')

    elif ((gfd[0x60:0x64] != inb[ftex_pos+0x24:ftex_pos+0x28]) or (gfd[0x60:0x64] != gfd[0xF0:0xF4])):
        messagebox.showinfo("", "Data size mismatch")
        os.remove(name + '2.gtx')

    elif gfd[0x68:0x6C] != inb[ftex_pos+0x2C:ftex_pos+0x30]:
        messagebox.showinfo("", "Mipmap size mismatch")
        os.remove(name + '2.gtx')

    elif gfd[0x54:0x58] != inb[ftex_pos+0x18:ftex_pos+0x1C]:
        messagebox.showinfo("", "Format mismatch")
        os.remove(name + '2.gtx')

    else:
        inb = bytearray(inb)

        inb[ftex_pos+0x04:ftex_pos+0x8C] = gfd[0x40:0xC8]

        dataSize = struct.unpack(">I", gfd[0x60:0x64])[0]
        mipSize = struct.unpack(">I", gfd[0x68:0x6C])[0]

        data_pos = struct.unpack(">I", bytes(inb[ftex_pos+0xB0:ftex_pos+0xB4]))[0] + ftex_pos + 0xB0
        mip_pos = struct.unpack(">I", bytes(inb[ftex_pos+0xB4:ftex_pos+0xB8]))[0]

        inb[data_pos:data_pos+dataSize] = gfd[0xFC:0xFC+dataSize]

        if mip_pos == 0:
            pass
        else:
            mip_pos += ftex_pos + 0xB4
            inb[mip_pos:mip_pos+mipSize] = gfd[0xFC+dataSize+0x20:0xFC+dataSize+0x20+mipSize]

        with open(bfres, "wb") as output:
            output.write(inb)
            output.close()

        os.remove(name + '2.gtx')

        messagebox.showinfo("", "Done!")

def openfile():
    options = {}
    options['filetypes'] = [('BFRES files', '.bfres')]
    filename = askopenfilename(parent=top, filetypes=options['filetypes'])

    with open(filename, "rb") as inf:
        inb = inf.read()
        inf.close()

    global menubar
    global filemenu
    
    if inb[:4] != b"FRES":
        messagebox.showinfo("", "Invalid BFRES header!")
    else:
        group = groups()
        group.pos = struct.unpack(">I", inb[0x24:0x28])[0]

        if group.pos == 0:
            messagebox.showinfo("", "No textures found in this BFRES file!")
        else:
            group.pos += 0x24
            group.file = struct.unpack(">I", inb[group.pos+4:(group.pos+4)+4])[0]

            group.name_pos = []
            group.name = []
            group.data_pos = []

            for i in range(group.file + 1):
                group.name_pos.append(struct.unpack(">I", inb[group.pos+8+(0x10*i)+8:(group.pos+8+(0x10*i)+8)+4])[0])
                group.data_pos.append(struct.unpack(">I", inb[group.pos+8+(0x10*i)+12:(group.pos+8+(0x10*i)+12)+4])[0])
                        

                if group.data_pos[i] == 0:
                    group.name.append("")
                else:
                    group.name_pos[i] += group.pos + 8 + (0x10*i) + 8
                    group.data_pos[i] += group.pos + 8 + (0x10*i) + 12
                    group.name.append(find_name(inb, group.name_pos[i]))

            folder = os.path.dirname(os.path.abspath(filename))

            scr = Scrollbar(top, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scr.set)

            scr.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4,4), window=frame, anchor="nw")

            frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

            options['filetypes'] = [('DDS files', '.dds')]

            for i in range(group.file):
                ftex_pos = group.data_pos[i + 1]
                name = group.name[i + 1]
                if os.path.isfile(folder + "\\" + name + ".dds"):
                    format_ = struct.unpack(">I", inb[ftex_pos+0x18:ftex_pos+0x1C])[0]

                else:
                    format_ = FTEXtoDDS(ftex_pos, inb, name, folder)

                if format_ in formats:
                    tv = 'Replace "' + name + '"\n' + formats2[format_]
                    b = Button(frame, text=tv, command=lambda ftex_pos=ftex_pos: DDStoBFRES(ftex_pos, askopenfilename(parent=top, filetypes=options['filetypes']), filename))
                    b.pack(padx=1, pady=1)
            
            menubar.destroy()
            filemenu.destroy()

            messagebox.showinfo("", "Done!")

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def main():
    global tex
    global scr

    print("(C) 2017 AboodXD")

    down = False

    if not os.path.isfile("C:/Tex/new.txt"):
        down = True
    else:
        with open("C:/Tex/new.txt", "r") as txt:
            if txt.read() != 'v3.1':
                down = True

    if down:
        warnings.filterwarnings("ignore")

        print("")
        print("Downloading the necessary tools...")

        if not os.path.isdir("C:\Tex"):
            os.mkdir("C:\Tex")

        print("")
        print("Fetching GTX Extractor (C ver.)... ")
        print("")
        response = requests.get('https://github.com/aboood40091/RandomStuff/', verify=False)

        if (int(response.status_code)) == 200:
            print("Connected to the download page!")

        else:
            response = requests.get('https://www.google.com', verify=False)
            if (int(response.status_code)) == 200:
                print("")
                print("It seems that the download page is down. Try restarting BFRES Tool and check if it still doesn't work.")
                print("")
                print("Exiting in 5 seconds...")
                time.sleep(5)
                sys.exit(1)

            else:
                print("")
                print("It looks like you don't have a working internet connection. Connect to another network, or solve the connection problem.")
                print("")
                print("Exiting in 5 seconds...")
                time.sleep(5)
                sys.exit(1)

        source = "gtx_extract.exe"
        destination = "C:/Tex"

        if not os.path.isfile(destination + '/' + source):
            os.remove(destination + '/' + source)

        print("")
        print("Downloading...")
        urllib.request.urlretrieve("https://github.com/aboood40091/RandomStuff/releases/download/v0.1/gtx_extract_no5.exe", "gtx_extract.exe")
        print("Download completed!")

        print("")
        print("Moving files...")
        
        if not os.path.isfile(destination + '/' + source):
            shutil.move(source, destination)

        print("")
        print("Fetching TexConv2... ")
        print("")
        response = requests.get('https://github.com/aboood40091/WiiUTools/tree/master/TexHaxU', verify=False)

        if (int(response.status_code)) == 200:
            print("Connected to the download page!")

        else:
            response = requests.get('https://www.google.com', verify=False)
            if (int(response.status_code)) == 200:
                print("")
                print("It seems that the download page is down. Try restarting BFRES Tool and check if it still doesn't work.")
                print("")
                print("Exiting in 5 seconds...")
                time.sleep(5)
                sys.exit(1)

            else:
                print("")
                print("It looks like you don't have a working internet connection. Connect to another network, or solve the connection problem.")
                print("")
                print("Exiting in 5 seconds...")
                time.sleep(5)
                sys.exit(1)

        source1 = "gfd.dll"
        source2 = "TexConv2.exe"
        source3 = "texUtils.dll"
        destination = "C:/Tex"

        if os.path.isfile(destination + '/' + source1):
            os.remove(destination + '/' + source1)

        if os.path.isfile(destination + '/' + source2):
            os.remove(destination + '/' + source2)

        if os.path.isfile(destination + '/' + source3):
            os.remove(destination + '/' + source3)

        print("")
        print("Downloading...")
        urllib.request.urlretrieve("https://github.com/aboood40091/WiiUTools/raw/master/TexHaxU/gfd.dll", "gfd.dll")
        urllib.request.urlretrieve("https://github.com/aboood40091/WiiUTools/raw/master/TexHaxU/TexConv2.exe", "TexConv2.exe")
        urllib.request.urlretrieve("https://github.com/aboood40091/WiiUTools/raw/master/TexHaxU/texUtils.dll", "texUtils.dll")
        print("Download completed!")

        print("")
        print("Moving files...")
        
        if not os.path.isfile(destination + '/' + source1):
            shutil.move(source1, destination)

        if not os.path.isfile(destination + '/' + source2):
            shutil.move(source2, destination)

        if not os.path.isfile(destination + '/' + source3):
            shutil.move(source3, destination)

        with open("C:/Tex/new.txt", "w+") as txt:
            txt.write('v3.1')
            txt.close()
        
    top.title("BFRES Tool v3.1")
    filemenu.add_command(label="Open", command=openfile)
    menubar.add_cascade(label="File", menu=filemenu)

    top.config(menu=menubar)
    top.mainloop()

if __name__ == '__main__': main()
