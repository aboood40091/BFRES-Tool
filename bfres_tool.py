#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFRES Tool
# Version 0.2
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

def err():
    print("")
    print("Usage (BFRES to GTX): python bfres_tool.py bfres")
    print("Usage (GTX to BFRES): python bfres_tool.py gtx bfres offset")
    print("")
    print("Exiting in 5 seconds...")
    time.sleep(5)
    sys.exit(1)

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

def FTEXtoGTX(ftex_pos, f, name, folder):
    ftex = f[ftex_pos:ftex_pos+0xC0]

    head1 = bytearray.fromhex("4766783200000020000000070000000100000002000000000000000000000000424C4B7B0000002000000001000000000000000B0000009C0000000000000000")
    head4 = bytearray.fromhex("424C4B7B00000020000000010000000000000001000000000000000000000000")

    info = ftex[0x4:0xA0]

    dataSize = struct.unpack(">I", info[0x20:0x24])[0]
    mipSize = struct.unpack(">I", info[0x28:0x2C])[0]

    head2 = bytearray.fromhex("424C4B7B0000002000000001000000000000000C") + dataSize.to_bytes(4, 'big') + bytearray.fromhex("0000000000000000")
    head3 = bytearray.fromhex("424C4B7B0000002000000001000000000000000D") + mipSize.to_bytes(4, 'big') + bytearray.fromhex("0000000000000000")

    data_pos = struct.unpack(">I", f[ftex_pos+0xB0:ftex_pos+0xB4])[0] + ftex_pos + 0xB0
    mip_pos = struct.unpack(">I", f[ftex_pos+0xB4:ftex_pos+0xB8])[0] + ftex_pos + 0xB4

    data = f[data_pos:data_pos+dataSize]

    if mip_pos == 0:
        head3 = b""
        mip = b""
    else:
        mip = f[mip_pos:mip_pos+mipSize]

    file = head1 + info + head2 + data + head3 + mip + head4

    with open(folder + "\\" + name + ".gtx", "wb") as output:
        output.write(file)
        output.close()

def GTXtoBFRES(ftex_pos, gtx, bfres):
    with open(bfres, "rb") as inf:
        inb = inf.read()
        inf.close()

    with open(gtx, "rb") as gfd1:
        gfd = gfd1.read()
        gfd1.close()

    if inb[:4] != b"FRES":
        print("")
        print("Invalid BFRES header!")
        print("")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    if gfd[:4] != b"Gfx2":
        print("")
        print("Invalid GTX header!")
        print("")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    if ((gfd[0x60:0x64] != inb[ftex_pos+0x24:ftex_pos+0x28]) or (gfd[0x60:0x64] != gfd[0xF0:0xF4])):
        print("")
        print("Data size mismatch")
        print("")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    if gfd[0x68:0x6C] != inb[ftex_pos+0x2C:ftex_pos+0x30]:
        print("")
        print("Mipmap size mismatch")
        print("")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    if gfd[0x54:0x58] != inb[ftex_pos+0x18:ftex_pos+0x1C]:
        print("")
        print("Format mismatch")
        print("")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    inb = bytearray(inb)

    inb[ftex_pos+0x04:ftex_pos+0xA0] = gfd[0x40:0xDC]

    dataSize = struct.unpack(">I", gfd[0x60:0x64])[0]
    mipSize = struct.unpack(">I", gfd[0x68:0x6C])[0]

    data_pos = struct.unpack(">I", bytes(inb[ftex_pos+0xB0:ftex_pos+0xB4]))[0] + ftex_pos + 0xB0
    mip_pos = struct.unpack(">I", bytes(inb[ftex_pos+0xB4:ftex_pos+0xB8]))[0] + ftex_pos + 0xB4

    inb[data_pos:data_pos+dataSize] = gfd[0xFC:0xFC+dataSize]

    if mip_pos == 0:
        pass
    else:
        inb[mip_pos:mip_pos+mipSize] = gfd[0xFC+dataSize+0x20:0xFC+dataSize+0x20+mipSize]

    with open(bfres, "wb") as output:
        output.write(inb)
        output.close()

def main():

    print("BFRES Tool v0.2")
    print("(C) 2017 AboodXD")
    
    if ((len(sys.argv) != 2) or (not sys.argv[1].endswith(".bfres"))):
        if ((len(sys.argv) != 4) or (not sys.argv[1].endswith(".gtx")) or (not sys.argv[2].endswith(".bfres"))):
            err()

    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as inf:
            inb = inf.read()
            inf.close()

        if inb[:4] != b"FRES":
            print("")
            print("Invalid BFRES header!")
            print("")
            print("Exiting in 5 seconds...")
            time.sleep(5)
            sys.exit(1)

        group = groups()
        group.pos = struct.unpack(">I", inb[0x24:0x28])[0]

        if group.pos == 0:
            print("")
            print("No textures found")
            print("")
            print("Exiting in 5 seconds...")
            time.sleep(5)
            sys.exit(1)
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
                
                    print("")
                    print(group.name[i] + ": " + hex(group.data_pos[i]))

        folder = os.path.dirname(os.path.abspath(sys.argv[1]))

        for i in range(group.file):
            ftex_pos = group.data_pos[i + 1]
            name = group.name[i + 1]
            FTEXtoGTX(ftex_pos, inb, name, folder)
    else:
        print("")
        print("Injecting: " + sys.argv[1])
        ftex_pos = int(sys.argv[3], 16)

        GTXtoBFRES(ftex_pos, sys.argv[1], sys.argv[2])

if __name__ == '__main__': main()
