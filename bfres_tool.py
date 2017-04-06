#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Version 2.1
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
import zipfile

top = Tk()
canvas = Canvas(top)
frame = Frame(canvas)
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)

formats = {0x00000000: 'GX2_SURFACE_FORMAT_INVALID',
           0x00000001: 'GX2_SURFACE_FORMAT_TC_R8_UNORM',
           0x00000101: 'GX2_SURFACE_FORMAT_TC_R8_UINT',
           0x00000201: 'GX2_SURFACE_FORMAT_TC_R8_SNORM',
           0x00000301: 'GX2_SURFACE_FORMAT_TC_R8_SINT',
           0x00000002: 'GX2_SURFACE_FORMAT_T_R4_G4_UNORM',
           0x00000005: 'GX2_SURFACE_FORMAT_TCD_R16_UNORM',
           0x00000105: 'GX2_SURFACE_FORMAT_TC_R16_UINT',
           0x00000205: 'GX2_SURFACE_FORMAT_TC_R16_SNORM',
           0x00000305: 'GX2_SURFACE_FORMAT_TC_R16_SINT',
           0x00000806: 'GX2_SURFACE_FORMAT_TC_R16_FLOAT',
           0x00000007: 'GX2_SURFACE_FORMAT_TC_R8_G8_UNORM',
           0x00000107: 'GX2_SURFACE_FORMAT_TC_R8_G8_UINT',
           0x00000207: 'GX2_SURFACE_FORMAT_TC_R8_G8_SNORM',
           0x00000307: 'GX2_SURFACE_FORMAT_TC_R8_G8_SINT',
           0x00000008: 'GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM',
           0x0000000a: 'GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM',
           0x0000000b: 'GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM',
           0x0000000c: 'GX2_SURFACE_FORMAT_TC_A1_B5_G5_R5_UNORM',
           0x0000010d: 'GX2_SURFACE_FORMAT_TC_R32_UINT',
           0x0000030d: 'GX2_SURFACE_FORMAT_TC_R32_SINT',
           0x0000080e: 'GX2_SURFACE_FORMAT_TCD_R32_FLOAT',
           0x0000000f: 'GX2_SURFACE_FORMAT_TC_R16_G16_UNORM',
           0x0000010f: 'GX2_SURFACE_FORMAT_TC_R16_G16_UINT',
           0x0000020f: 'GX2_SURFACE_FORMAT_TC_R16_G16_SNORM',
           0x0000030f: 'GX2_SURFACE_FORMAT_TC_R16_G16_SINT',
           0x00000810: 'GX2_SURFACE_FORMAT_TC_R16_G16_FLOAT',
           0x00000011: 'GX2_SURFACE_FORMAT_D_D24_S8_UNORM',
           0x00000011: 'GX2_SURFACE_FORMAT_T_R24_UNORM_X8',
           0x00000111: 'GX2_SURFACE_FORMAT_T_X24_G8_UINT',
           0x00000811: 'GX2_SURFACE_FORMAT_D_D24_S8_FLOAT',
           0x00000816: 'GX2_SURFACE_FORMAT_TC_R11_G11_B10_FLOAT',
           0x00000019: 'GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM',
           0x00000119: 'GX2_SURFACE_FORMAT_TC_R10_G10_B10_A2_UINT',
           0x00000219: 'GX2_SURFACE_FORMAT_T_R10_G10_B10_A2_SNORM',
           0x00000219: 'GX2_SURFACE_FORMAT_TC_R10_G10_B10_A2_SNORM',
           0x00000319: 'GX2_SURFACE_FORMAT_TC_R10_G10_B10_A2_SINT',
           0x0000001a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM',
           0x0000011a: 'GX2_SURFACE_FORMAT_TC_R8_G8_B8_A8_UINT',
           0x0000021a: 'GX2_SURFACE_FORMAT_TC_R8_G8_B8_A8_SNORM',
           0x0000031a: 'GX2_SURFACE_FORMAT_TC_R8_G8_B8_A8_SINT',
           0x0000041a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB',
           0x0000001b: 'GX2_SURFACE_FORMAT_TCS_A2_B10_G10_R10_UNORM',
           0x0000011b: 'GX2_SURFACE_FORMAT_TC_A2_B10_G10_R10_UINT',
           0x0000081c: 'GX2_SURFACE_FORMAT_D_D32_FLOAT_S8_UINT_X24',
           0x0000081c: 'GX2_SURFACE_FORMAT_T_R32_FLOAT_X8_X24',
           0x0000011c: 'GX2_SURFACE_FORMAT_T_X32_G8_UINT_X24',
           0x0000011d: 'GX2_SURFACE_FORMAT_TC_R32_G32_UINT',
           0x0000031d: 'GX2_SURFACE_FORMAT_TC_R32_G32_SINT',
           0x0000081e: 'GX2_SURFACE_FORMAT_TC_R32_G32_FLOAT',
           0x0000001f: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_UNORM',
           0x0000011f: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_UINT',
           0x0000021f: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_SNORM',
           0x0000031f: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_SINT',
           0x00000820: 'GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_FLOAT',
           0x00000122: 'GX2_SURFACE_FORMAT_TC_R32_G32_B32_A32_UINT',
           0x00000322: 'GX2_SURFACE_FORMAT_TC_R32_G32_B32_A32_SINT',
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
           0x00000235: 'GX2_SURFACE_FORMAT_T_BC5_SNORM',
           0x00000081: 'GX2_SURFACE_FORMAT_T_NV12_UNORM'}

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

    head1 = bytearray.fromhex("4766783200000020000000070000000100000002000000000000000000000000424C4B7B0000002000000001000000000000000B0000009C0000000000000000")
    head4 = bytearray.fromhex("424C4B7B00000020000000010000000000000001000000000000000000000000")

    info = ftex[0x4:0x8C] + bytearray.fromhex("0000000000000000000000000000000000000000")

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

    print("")
    os.system('Tex\TexConv2.exe -i "' + folder + "\\" + name + '2.gtx" -f GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM -o "' + folder + "\\" + name + '.gtx"')
    os.system('Tex\gtx_extract.exe "' + folder + "\\" + name + '.gtx"')
    os.system('DEL "' + folder + "\\" + name + '.gtx"')
    os.system('DEL "' + folder + "\\" + name + '2.gtx"')

def DDStoBFRES(ftex_pos, dds, bfres):
    with open(bfres, "rb") as inf:
        inb = inf.read()
        inf.close()

    name = os.path.splitext(dds)[0]

    os.system('Tex\TexConv2.exe -i "' + dds + '" -o "' + name + '.gtx"')

    swizzle = struct.unpack(">I", inb[ftex_pos+0x38:ftex_pos+0x3C])[0]
    swizzle = (swizzle & 0xFFF) >> 8
    format_ = struct.unpack(">I", inb[ftex_pos+0x18:ftex_pos+0x1C])[0]
    tileMode = struct.unpack(">I", inb[ftex_pos+0x34:ftex_pos+0x38])[0]
    numMips = struct.unpack(">I", inb[ftex_pos+0x14:ftex_pos+0x18])[0]

    if numMips > 1:
        os.system('Tex\TexConv2.exe -i "' + name + '.gtx" -f ' + formats[format_] + ' -tileMode ' + tileModes[tileMode] + ' -swizzle ' + str(swizzle) + ' -mipFilter box -minmip 1 -o "' + name + '2.gtx"')
    else:
        os.system('Tex\TexConv2.exe -i "' + name + '.gtx" -f ' + formats[format_] + ' -tileMode ' + tileModes[tileMode] + ' -swizzle ' + str(swizzle) + ' -o "' + name + '2.gtx"')

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
                    pass
                else:
                    FTEXtoDDS(ftex_pos, inb, name, folder)

                tv = 'Replace "' + name + '"'
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

    if not os.path.isfile("Tex\gtx_extract.exe"):
        print("")
        print("Downloading the necessary tools...")

        if not os.path.isdir("C:\Program Files (x86)"):
            print("")
            print("It seems like you have a 32-bit computer... Good luck getting this to work on it!")

        else:
            if not os.path.isdir("Tex"):
                os.mkdir("Tex")

            print("")
            print("Fetching GTX Extractor... ")
            print("")
            response = requests.get('https://github.com/aboood40091/GTX-Extractor/')

            if (int(response.status_code)) == 200:
                print("Connected to the download page!")

            else:
                response = requests.get('https://www.google.com')
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

            print("")
            print("Downloading...")
            urllib.request.urlretrieve("https://github.com/aboood40091/GTX-Extractor/releases/download/v4.0/gtx_extract_x64_v4.0.zip", "gtx_extract.zip")
            print("Download completed!")
            print("")
            print("Unzipping...")
            
            zip = zipfile.ZipFile(r'gtx_extract.zip')  
            zip.extractall(r'Tex')
            
            print("File succesfully unzipped!")
            print("")
            print("Removing zipped file...")
            
            zip.close()
            os.remove("gtx_extract.zip")
            
            print("Zipped file succesfully removed!")

        if not os.path.isfile("Tex\TexConv2.exe"):
            print("")
            print("Fetching TexConv2... ")
            print("")
            response = requests.get('https://github.com/NWPlayer123/WiiUTools/tree/master/TexHaxU')

            if (int(response.status_code)) == 200:
                print("Connected to the download page!")

            else:
                response = requests.get('https://www.google.com')
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

            print("")
            print("Downloading...")
            urllib.request.urlretrieve("https://github.com/NWPlayer123/WiiUTools/raw/master/TexHaxU/gfd.dll", "gfd.dll")
            urllib.request.urlretrieve("https://github.com/NWPlayer123/WiiUTools/raw/master/TexHaxU/TexConv2.exe", "TexConv2.exe")
            urllib.request.urlretrieve("https://github.com/NWPlayer123/WiiUTools/raw/master/TexHaxU/texUtils.dll", "texUtils.dll")
            print("Download completed!")

            print("")
            print("Moving files...")
            source1 = "gfd.dll"
            source2 = "TexConv2.exe"
            source3 = "texUtils.dll"
            destination = "Tex"
            
            shutil.move(source1, destination)
            shutil.move(source2, destination)
            shutil.move(source3, destination)
        
    top.title("BFRES Tool v2.1")
    filemenu.add_command(label="Open", command=openfile)
    menubar.add_cascade(label="File", menu=filemenu)

    top.config(menu=menubar)
    top.mainloop()

if __name__ == '__main__': main()
