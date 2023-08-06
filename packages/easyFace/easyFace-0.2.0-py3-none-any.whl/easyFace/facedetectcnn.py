#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import ctypes
import platform
from pathlib import Path
from typing import List, Tuple, Union
import sys

import numpy as np
from PIL import Image as PIL
from PIL.Image import Image

if platform.system() == 'Windows':
    # load .dll for Windows
    if '32 bit' in sys.version:
        LoadDLL = ctypes.cdll.LoadLibrary
    else:
        LoadDLL = ctypes.WinDLL
else:
    # load lib for Linux, Darwin, etc
    LoadDLL = ctypes.cdll.LoadLibrary

arch = platform.architecture()[0]
if platform.system() == 'Windows':
    # this dll is compiled from modified code
    # which keeps the function name unmangled
    # the dll is compiled in VS 2015 for x86
    # with ENABLE_AVX2 option on to speed up
    current_dir = Path(__file__).parent
    dll_name = 'libfacedetection_{0}.{1}'
    dll_name = dll_name.format(arch, 'dll')
    path = Path(current_dir / dll_name)
    dll = LoadDLL(path.resolve().as_posix())
elif platform.system() == 'Linux':
    if platform.uname().node == 'raspberrypi':
        current_dir = Path(__file__).parent
        dll_name = 'libfacedetection_{0}.{1}'
        dll_name = dll_name.format('raspbian', 'so')
        path = Path(current_dir / dll_name)
        dll = LoadDLL(path.resolve().as_posix())
    else:
        # the dll the compiled using gcc for x86
        # with ENABLE_AVX2 option on to speed up
        current_dir = Path(__file__).parent
        dll_name = 'libfacedetection_{0}.{1}'
        dll_name = dll_name.format(arch, 'so')
        path = Path(current_dir / dll_name)
        dll = LoadDLL(path.resolve().as_posix())
elif platform.system() == 'Darwin':
    # TODO: Darwin support
    raise NotImplementedError
else:
    # TODO: BSD support, etc
    raise NotImplementedError

# THE SIGNATURE OF facedetect_cnn
# unsigned char * result_buffer
# unsigned char * rgb_image_data
# int width, int height, int step
if platform.uname().node == 'raspberrypi':
    dll._Z14facedetect_cnnPhS_iii.restype = ctypes.POINTER(ctypes.c_int)
    dll._Z14facedetect_cnnPhS_iii.argtypes = [ctypes.POINTER(ctypes.c_ubyte),
                                   ctypes.POINTER(ctypes.c_ubyte),
                                   ctypes.c_int, ctypes.c_int, ctypes.c_int]
else:
    dll.facedetect_cnn.restype = ctypes.POINTER(ctypes.c_int)
    dll.facedetect_cnn.argtypes = [ctypes.POINTER(ctypes.c_ubyte),
                                   ctypes.POINTER(ctypes.c_ubyte),
                                   ctypes.c_int, ctypes.c_int, ctypes.c_int]

# Faces: [(x y width height confidence angle)]
Faces = List[Tuple[int, int, int, int, int]]
c_ubyte_p = ctypes.POINTER(ctypes.c_ubyte)
c_short_p = ctypes.POINTER(ctypes.c_short)
c_int_p = ctypes.POINTER(ctypes.c_int)


# noinspection PyTypeChecker
# noinspection PyUnresolvedReferences
# noinspection PyCallingNonCallable
def cfacedetect_cnn(image: bytes,
                    width: int,
                    height: int,
                    step: int) -> Faces:
    image_type = ctypes.c_ubyte * (step * height)
    image_data = image_type.from_buffer_copy(image)
    # the magic number 0x20000 is DETECT_BUFFER_SIZE
    # which used in the original example source code
    result_buffer = (ctypes.c_ubyte * 0x20000)()
    # the return value is (int *)(result_buffer)
    # so just ignore it and use the result_buffer
    if platform.uname().node == 'raspberrypi':
        dll._Z14facedetect_cnnPhS_iii(result_buffer, image_data,
                       width, height, step)
    else:
        dll.facedetect_cnn(result_buffer, image_data,
                       width, height, step)
    length = ctypes.cast(result_buffer, c_int_p)[0]
    faces = ctypes.cast(result_buffer, c_short_p)
    faces_results = []
    if platform.uname().node == 'raspberrypi':
        for i in range(length):
            start_addr = 2 + 142 * i
            c = faces[start_addr]
            x = faces[start_addr + 1]
            y = faces[start_addr + 2]
            w = faces[start_addr + 3]
            h = faces[start_addr + 4]
            lm1 = faces[start_addr + 5]
            lm2 = faces[start_addr + 6]
            lm3 = faces[start_addr + 7]
            lm4 = faces[start_addr + 8]
            lm5 = faces[start_addr + 9]
            lm6 = faces[start_addr + 10]
            lm7 = faces[start_addr + 11]
            lm8 = faces[start_addr + 12]
            lm9 = faces[start_addr + 13]
            lm10 = faces[start_addr + 14]
            result = (x, y, w, h, c, lm1,lm2,lm3,lm4,lm5,lm6,lm7,lm8,lm9,lm10)
            faces_results.append(result)
    else:
        for i in range(length):
            start_addr = 2 + 142 * i
            x = faces[start_addr + 0]
            y = faces[start_addr + 1]
            w = faces[start_addr + 2]
            h = faces[start_addr + 3]
            c = faces[start_addr + 4]
            result = (x, y, w, h, c)
            faces_results.append(result)

    # since here is Python
    # no more length needed
    return faces_results


# noinspection PyTypeChecker
def facedetect_cnn(image: Union[str, Path, Image, np.ndarray, bytes],
                   width: int = 0, height: int = 0, step: int = 0) -> Faces:
    # if the image is filepath(str)
    # then build the absolute path
    if isinstance(image, str):
        image = Path(image)
        image = image.resolve()
    # if the given type is Path
    # then open the image by it
    if isinstance(image, Path):
        image = image.as_posix()
        image = PIL.open(image)
    # if the given type is PIL Image
    # then convert it from RGB to BGR
    if isinstance(image, Image):
        # if there is size given
        # then resize the image
        if width and height:
            size = (width, height)
            image = image.resize(size)
        image = image.convert('RGB')
        image = np.array(image)
        image = image[..., ::-1]
    # if the given type is numpy array
    # then calculate all the parameters
    if isinstance(image, np.ndarray):
        width = image.shape[1]
        height = image.shape[0]
        depth = image.shape[2]
        step = width * depth
        image = image.tobytes()
    # everything is ready, call the function for result
    return cfacedetect_cnn(image, width, height, step)


if __name__ == '__main__':
    # print(dll.facedetect_cnn)
    facedetect_cnn('lena512color.tiff')
