#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2016-2018 AboodXD

################################################################
################################################################


def rgb8torgbx8(data):
    numPixels = len(data) // 3

    new_data = bytearray(numPixels * 4)

    for i in range(numPixels):
        new_data[4 * i + 0] = data[3 * i + 0]
        new_data[4 * i + 1] = data[3 * i + 1]
        new_data[4 * i + 2] = data[3 * i + 2]
        new_data[4 * i + 3] = 0xFF

    return bytes(new_data)


def _swapRB_rgb565(pixel):
    red = pixel & 0x1F
    green = (pixel & 0x7E0) >> 5
    blue = (pixel & 0xF800) >> 11

    return (red << 11) | (green << 5) | blue


def _swapRB_rgb5a1(pixel):
    red = pixel & 0x1F
    green = (pixel & 0x3E0) >> 5
    blue = (pixel & 0x7c00) >> 10
    alpha = (pixel & 0x8000) >> 15

    return (alpha << 15) | (red << 10) | (green << 5) | blue


def _swapRB_rgba4(pixel):
    red = pixel & 0xF
    green = (pixel & 0xF0) >> 4
    blue = (pixel & 0xF00) >> 8
    alpha = (pixel & 0xF000) >> 12

    return (alpha << 12) | (red << 8) | (green << 4) | blue


def _swapRB_argb4(pixel):
    alpha = pixel & 0xF
    red = (pixel & 0xF0) >> 4
    green = (pixel & 0xF00) >> 8
    blue = (pixel & 0xF000) >> 12

    return (red << 12) | (green << 8) | (blue << 4) | alpha


def swapRB_16bpp(data, format_):
    numPixels = len(data) // 2

    new_data = bytearray(numPixels * 2)

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

    return bytes(new_data)


def rgba4_to_argb4(data):
    numPixels = len(data) // 2

    new_data = bytearray(numPixels * 2)

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

    return bytes(new_data)


def _swapRB_bgr10a2(pixel):
    red = (pixel & 0x3FF00000) >> 20
    green = (pixel & 0xFFC00) >> 10
    blue = pixel & 0x3FF
    alpha = (pixel & 0xC0000000) >> 30

    return (alpha << 30) | (blue << 20) | (green << 10) | red


def _swapRB_rgba8(pixel):
    red = pixel & 0xFF
    green = (pixel & 0xFF00) >> 8
    blue = (pixel & 0xFF0000) >> 16
    alpha = (pixel & 0xFF000000) >> 24

    return (alpha << 24) | (red << 16) | (green << 8) | blue


def swapRB_32bpp(data, format_):
    numPixels = len(data) // 4

    new_data = bytearray(numPixels * 4)

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

    return bytes(new_data)
