#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2016-2018 AboodXD

################################################################
################################################################

from cpython cimport array
from cython cimport view
from libc.stdlib cimport malloc, free


ctypedef unsigned char u8
ctypedef unsigned short u16
ctypedef unsigned int u32


cpdef bytes rgb8torgbx8(bytearray data):
    cdef:
        u32 numPixels = len(data) // 3

        u8 *new_data = <u8 *>malloc(numPixels * 4)
        u32 i

    try:
        for i in range(numPixels):
            new_data[4 * i + 0] = data[3 * i + 0]
            new_data[4 * i + 1] = data[3 * i + 1]
            new_data[4 * i + 2] = data[3 * i + 2]
            new_data[4 * i + 3] = 0xFF

        return bytes(<u8[:numPixels * 4]>new_data)

    finally:
        free(new_data)


cdef u16 _swapRB_rgb565(u16 pixel):
    cdef:
        u8 red = pixel & 0x1F
        u8 green = (pixel & 0x7E0) >> 5
        u8 blue = (pixel & 0xF800) >> 11

    return <u16>((red << 11) | (green << 5) | blue)


cdef u16 _swapRB_rgb5a1(u16 pixel):
    cdef:
        u8 red = pixel & 0x1F
        u8 green = (pixel & 0x3E0) >> 5
        u8 blue = (pixel & 0x7c00) >> 10
        u8 alpha = (pixel & 0x8000) >> 15

    return <u16>((alpha << 15) | (red << 10) | (green << 5) | blue)


cdef u16 _swapRB_rgba4(u16 pixel):
    cdef:
        u8 red = pixel & 0xF
        u8 green = (pixel & 0xF0) >> 4
        u8 blue = (pixel & 0xF00) >> 8
        u8 alpha = (pixel & 0xF000) >> 12

    return <u16>((alpha << 12) | (red << 8) | (green << 4) | blue)


cdef u16 _swapRB_argb4(u16 pixel):
    cdef:
        u8 alpha = pixel & 0xF
        u8 red = (pixel & 0xF0) >> 4
        u8 green = (pixel & 0xF00) >> 8
        u8 blue = (pixel & 0xF000) >> 12

    return <u16>((red << 12) | (green << 8) | (blue << 4) | alpha)


cpdef bytes swapRB_16bpp(bytes data, str format_):
    cdef:
        u32 numPixels = len(data) // 2

        u8 *new_data = <u8 *>malloc(numPixels * 2)
        u16 pixel, new_pixel
        u32 i

    try:
        for i in range(numPixels):
            pixel = (
                (data[2 * i + 1] << 8) |
                data[2 * i + 0]
            )

            if format_ == 'rgb565':
                new_pixel = _swapRB_rgb565(pixel)

            elif format_ == 'rgb5a1':
                new_pixel = _swapRB_rgb5a1(pixel)

            elif format_ == 'rgba4':
                new_pixel = _swapRB_rgba4(pixel)

            else:
                new_pixel = _swapRB_argb4(pixel)

            new_data[2 * i + 1] = (new_pixel & 0xFF00) >> 8
            new_data[2 * i + 0] = new_pixel & 0xFF

        return bytes(<u8[:numPixels * 2]>new_data)

    finally:
        free(new_data)


cpdef bytes rgba4_to_argb4(bytes data):
    cdef:
        u32 numPixels = len(data) // 2

        u8 *new_data = <u8 *>malloc(numPixels * 2)
        u8 alpha
        u16 rgb, pixel, new_pixel
        u32 i

    try:
        for i in range(numPixels):
            pixel = (
                (data[2 * i + 1] << 8) |
                data[2 * i + 0]
            )

            rgb = (pixel & 0xFFF)
            alpha = (pixel & 0xF000) >> 12

            new_pixel = (rgb << 4) | alpha

            new_data[2 * i + 1] = (new_pixel & 0xFF00) >> 8
            new_data[2 * i + 0] = new_pixel & 0xFF

        return bytes(<u8[:numPixels * 2]>new_data)

    finally:
        free(new_data)


cdef u32 _swapRB_bgr10a2(u32 pixel):
    cdef:
        u16 red = (pixel & 0x3FF00000) >> 20
        u16 green = (pixel & 0xFFC00) >> 10
        u16 blue = pixel & 0x3FF
        u8 alpha = (pixel & 0xC0000000) >> 30

    return <u32>((alpha << 30) | (blue << 20) | (green << 10) | red)


cdef u32 _swapRB_rgba8(u32 pixel):
    cdef:
        u8 red = pixel & 0xFF
        u8 green = (pixel & 0xFF00) >> 8
        u8 blue = (pixel & 0xFF0000) >> 16
        u8 alpha = (pixel & 0xFF000000) >> 24

    return <u32>((alpha << 24) | (red << 16) | (green << 8) | blue)


cpdef bytes swapRB_32bpp(bytes data, str format_):
    cdef:
        u32 numPixels = len(data) // 4

        u8 *new_data = <u8 *>malloc(numPixels * 4)
        u32 i, pixel, new_pixel

    try:
        for i in range(numPixels):
            pixel = (
                (data[4 * i + 3] << 24) |
                (data[4 * i + 2] << 16) |
                (data[4 * i + 1] << 8) |
                data[4 * i + 0]
            )

            if format_ == 'bgr10a2':
                new_pixel = _swapRB_bgr10a2(pixel)

            else:
                new_pixel = _swapRB_rgba8(pixel)

            new_data[4 * i + 3] = (new_pixel & 0xFF000000) >> 24
            new_data[4 * i + 2] = (new_pixel & 0xFF0000) >> 16
            new_data[4 * i + 1] = (new_pixel & 0xFF00) >> 8
            new_data[4 * i + 0] = new_pixel & 0xFF

        return bytes(<u8[:numPixels * 4]>new_data)

    finally:
        free(new_data)
