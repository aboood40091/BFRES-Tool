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

from math import ceil
import os.path
from PyQt5 import QtWidgets

from bytes import bytes_to_string
import addrlib
import dds
import bcn
import globals
from structs import struct, GX2Surface, empty


def read(file):
    with open(file, "rb") as inf:
        f = inf.read()

    if f[:4] != b"FRES" or f[4:8] == b'    ':
        QtWidgets.QMessageBox.warning(None, "Error", "Invalid file header!")
        return False

    version = f[4]

    if version not in [3, 4]:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported BFRES version!")
        return False

    group = empty()
    group.pos = struct.unpack(">i", f[0x24:0x28])[0]

    if group.pos == 0:
        return False

    group.pos += 0x28
    group.count = struct.unpack(">i", f[group.pos:group.pos + 4])[0]
    group.pos += 20

    textures = []
    texNames = []
    texSizes = []

    for i in range(group.count):
        nameAddr = struct.unpack(">i", f[group.pos + 16 * i + 8:group.pos + 16 * i + 12])[0]
        nameAddr += group.pos + 16 * i + 8

        name = bytes_to_string(f, nameAddr)

        pos = struct.unpack(">i", f[group.pos + 16 * i + 12:group.pos + 16 * i + 16])[0]
        pos += group.pos + 16 * i + 12

        ftex = empty()
        ftex.headAddr = pos

        pos += 4

        surface = GX2Surface()
        surface.data(f, pos)
        pos += surface.size

        if version == 4:
            surface.numMips = 1

        elif surface.numMips > 14:
            continue

        mipOffsets = []
        for j in range(13):
            mipOffsets.append(
                f[j * 4 + pos] << 24
                | f[j * 4 + 1 + pos] << 16
                | f[j * 4 + 2 + pos] << 8
                | f[j * 4 + 3 + pos]
            )

        pos += 68

        compSel = []
        compSel2 = []
        for j in range(4):
            comp = f[pos + j]
            compSel2.append(comp)
            if comp == 4:  # Sorry, but this is unsupported.
                comp = j

            compSel.append(comp)

        pos += 24

        ftex.name = name
        ftex.dim = surface.dim
        ftex.width = surface.width
        ftex.height = surface.height
        ftex.depth = surface.depth
        ftex.numMips = surface.numMips
        ftex.format = surface.format_
        ftex.aa = surface.aa
        ftex.use = surface.use
        ftex.imageSize = surface.imageSize
        ftex.imagePtr = surface.imagePtr
        ftex.mipSize = surface.mipSize
        ftex.mipPtr = surface.mipPtr
        ftex.tileMode = surface.tileMode
        ftex.swizzle = surface.swizzle
        ftex.alignment = surface.alignment
        ftex.pitch = surface.pitch
        ftex.compSel = compSel
        ftex.compSel2 = compSel2
        ftex.mipOffsets = mipOffsets

        ftex.surfInfo = addrlib.getSurfaceInfo(ftex.format, ftex.width, ftex.height, ftex.depth, ftex.dim, ftex.tileMode, ftex.aa, 0)

        if ftex.format in globals.BCn_formats:
            ftex.blkWidth, ftex.blkHeight = 4, 4

        else:
            ftex.blkWidth, ftex.blkHeight = 1, 1

        ftex.bpp = addrlib.surfaceGetBitsPerPixel(surface.format_) // 8

        dataAddr = struct.unpack(">i", f[ftex.headAddr + 0xB0:ftex.headAddr + 0xB4])[0]
        dataAddr += ftex.headAddr + 0xB0

        ftex.dataAddr = dataAddr
        ftex.data = f[dataAddr:dataAddr + ftex.imageSize]

        mipAddr = struct.unpack(">i", f[ftex.headAddr + 0xB4:ftex.headAddr + 0xB8])[0]
        if mipAddr and ftex.mipSize:
            mipAddr += ftex.headAddr + 0xB4
            ftex.mipData = f[mipAddr:mipAddr + ftex.mipSize]

        else:
            ftex.mipData = b''

        textures.append(ftex)
        texNames.append(name)
        texSizes.append([ftex.imageSize, ftex.mipSize])

    globals.fileData = bytearray(f)
    globals.texSizes = texSizes

    return textures, texNames


def decode(tex):
    surfInfo = tex.surfInfo
    data = tex.data[:surfInfo.surfSize]

    result = []
    for mipLevel in range(tex.numMips):
        width = max(1, tex.width >> mipLevel)
        height = max(1, tex.height >> mipLevel)

        size = ceil(width / tex.blkWidth) * ceil(height / tex.blkHeight) * tex.bpp

        if mipLevel != 0:
            mipOffset = tex.mipOffsets[mipLevel - 1]
            if mipLevel == 1:
                mipOffset -= surfInfo.surfSize

            surfInfo = addrlib.getSurfaceInfo(tex.format, tex.width, tex.height, tex.depth, tex.dim, tex.tileMode, tex.aa, mipLevel)
            data = tex.mipData[mipOffset:mipOffset + surfInfo.surfSize]

        result_ = addrlib.deswizzle(
            width, height, surfInfo.height, tex.format, surfInfo.tileMode,
            tex.swizzle, surfInfo.pitch, surfInfo.bpp, data,
        )

        result.append(result_[:size])

    return result


def extract(tex, BFRESPath, exportAs, dontShowMsg=False):
    if tex.format in globals.formats and not tex.aa and tex.surfInfo.depth == 1:
        if (tex.format & 0xFF) == 0x1a:
            format_ = "rgba8"

        elif tex.format == 0x19:
            format_ = "bgr10a2"

        elif tex.format == 0x8:
            format_ = "rgb565"

        elif tex.format == 0xa:
            format_ = "rgb5a1"

        elif tex.format == 0xb:
            format_ = "rgba4"

        elif tex.format == 0x1:
            format_ = "l8"

        elif tex.format == 0x7:
            format_ = "la8"

        elif tex.format == 0x2:
            format_ = "la4"

        elif (tex.format & 0xFF) == 0x31:
            format_ = "BC1"

        elif (tex.format & 0xFF) == 0x32:
            format_ = "BC2"

        elif (tex.format & 0xFF) == 0x33:
            format_ = "BC3"

        elif tex.format == 0x34:
            format_ = "BC4U"

        elif tex.format == 0x234:
            format_ = "BC4S"

        elif tex.format == 0x35:
            format_ = "BC5U"

        elif tex.format == 0x235:
            format_ = "BC5S"

        realSize = ceil(tex.width / tex.blkWidth) * ceil(tex.height / tex.blkWidth) * tex.bpp
        result = decode(tex)

        if exportAs:
            file = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "DDS (*.dds)")[0]
            if not file:
                return False

        else:
            file = os.path.join(BFRESPath, tex.name + '.dds')

        hdr = dds.generateHeader(tex.numMips, tex.width, tex.height, format_, tex.compSel, realSize, tex.format in globals.BCn_formats)

        with open(file, "wb+") as output:
            output.write(b''.join([hdr, b''.join(result)]))

    elif not dontShowMsg:
        msg = "Can't convert: " + tex.name

        if tex.aa:
            context = "Unsupported AA mode."

        elif tex.surfInfo.depth != 1:
            context = "Unsupported depth."

        else:
            context = "Format is not supported."

        QtWidgets.QMessageBox.warning(None, "Error", '\n'.join([msg, context]))
        return False


def roundUp(x, y):
    return ((x - 1) | (y - 1)) + 1


def getCurrentMipOffset_Size(width, height, blkWidth, blkHeight, bpp, currLevel):
    offset = 0

    for mipLevel in range(currLevel):
        width_ = ceil(max(1, width >> mipLevel) / blkWidth)
        height_ = ceil(max(1, height >> mipLevel) / blkHeight)

        offset += width_ * height_ * bpp

    width_ = ceil(max(1, width >> currLevel) / blkWidth)
    height_ = ceil(max(1, height >> currLevel) / blkHeight)

    size = width_ * height_ * bpp

    return offset, size


def inject(tex, tileMode, swizzle_, SRGB, importMips, oldImageSize, oldMipSize, f):
    width, height, format_, fourcc, dataSize, compSel, numMips, data = dds.readDDS(f, SRGB)

    if 0 in [width, dataSize] and data == []:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported DDS file.")
        return False

    if format_ not in globals.formats:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported DDS format.")
        return False

    elif numMips > 13:
        QtWidgets.QMessageBox.warning(None, "Error", "Invalid number of mipmaps.")
        return False

    if not importMips:
        numMips = 1

    else:
        if tex.numMips < numMips + 1:
            QtWidgets.QMessageBox.warning(
                None, "Warning",
                "This DDS file has more mipmaps (%d) than the original image (%d)!\n"
                "Not all mipmaps might be imported." % (numMips, tex.numMips - 1),
            )

        numMips += 1

    bpp = addrlib.surfaceGetBitsPerPixel(format_) // 8
    surfInfo = addrlib.getSurfaceInfo(format_, width, height, 1, 1, tileMode, 0, 0)

    if surfInfo.depth != 1:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported depth.")
        return False

    elif surfInfo.surfSize > oldImageSize:
        QtWidgets.QMessageBox.warning(
            None, "Error",
            'This DDS has a larger filesize than the original image!',
        )

        return False

    tex.surfInfo = surfInfo

    alignment = surfInfo.baseAlign
    imageSize = surfInfo.surfSize
    pitch = surfInfo.pitch

    if tileMode in [1, 2, 3, 16]:
        s = swizzle_ << 8

    else:
        s = 0xd0000 | swizzle_ << 8

    if format_ in globals.BCn_formats:
        blkWidth, blkHeight = 4, 4

    else:
        blkWidth, blkHeight = 1, 1

    mipSize = 0
    numMips_ = 1
    mipOffsets = []

    result = []
    for mipLevel in range(numMips):
        offset, size = getCurrentMipOffset_Size(width, height, blkWidth, blkHeight, bpp, mipLevel)
        data_ = data[offset:offset + size]

        width_ = max(1, width >> mipLevel)
        height_ = max(1, height >> mipLevel)

        if mipLevel:
            surfInfo = addrlib.getSurfaceInfo(format_, width, height, 1, 1, tileMode, 0, mipLevel)

            if mipLevel == 1:
                mipOffsets.append(imageSize)

            else:
                mipOffsets.append(mipSize)

        data_ += b'\0' * (surfInfo.surfSize - size)
        dataAlignBytes = b'\0' * (roundUp(mipSize, surfInfo.baseAlign) - mipSize)

        if mipLevel:
            mipSize += surfInfo.surfSize + len(dataAlignBytes)

        if mipSize > oldMipSize:
            break

        result.append(bytearray(dataAlignBytes) + addrlib.swizzle(
            width_, height_, surfInfo.height, format_, surfInfo.tileMode,
            s, surfInfo.pitch, surfInfo.bpp, data_))

    tex.dim = 1
    tex.width = width
    tex.height = height
    tex.depth = 1
    tex.numMips = mipLevel
    tex.format = format_
    tex.aa = 0
    tex.use = 1
    tex.imageSize = imageSize
    tex.mipSize = mipSize
    tex.tileMode = tileMode
    tex.swizzle = s
    tex.alignment = alignment
    tex.pitch = pitch
    tex.compSel = tex.compSel2 = compSel
    tex.mipOffsets = mipOffsets
    tex.blkWidth, tex.blkHeight = blkWidth, blkHeight
    tex.bpp = bpp
    tex.data = bytes(result[0])
    tex.mipData = b''.join(result[1:])

    return tex


def writeTex(file, tex):
    surface = bytearray(GX2Surface().pack(
        tex.dim,
        tex.width,
        tex.height,
        tex.depth,
        tex.numMips,
        tex.format,
        tex.aa,
        tex.use,
        tex.imageSize,
        0,
        tex.mipSize,
        0,
        tex.tileMode,
        tex.swizzle,
        tex.alignment,
        tex.pitch,
    ))

    if tex.numMips > 1:
        for offset in tex.mipOffsets:
            surface += offset.to_bytes(4, 'big')

        surface += b'\0' * (15 - tex.numMips) * 4

    else:
        surface += b'\0' * 56

    surface += tex.numMips.to_bytes(4, 'big')
    surface += b'\0' * 4
    surface += 1 .to_bytes(4, 'big')

    for comp in tex.compSel:
        surface += bytes([comp])

    surface += b'\0' * 20

    ftexPos = tex.headAddr
    globals.fileData[ftexPos + 4:ftexPos + 0xA0] = surface

    dataAddr = struct.unpack(">i", globals.fileData[ftexPos + 0xB0:ftexPos + 0xB4])[0] + ftexPos + 0xB0
    mipAddr = struct.unpack(">i", globals.fileData[ftexPos + 0xB4:ftexPos + 0xB8])[0]

    globals.fileData[dataAddr:dataAddr + tex.imageSize] = tex.data

    if mipAddr:
        mipAddr += ftexPos + 0xB4
        globals.fileData[mipAddr:mipAddr + tex.mipSize] = tex.mipData

    with open(file, "wb+") as out:
        out.write(globals.fileData)
