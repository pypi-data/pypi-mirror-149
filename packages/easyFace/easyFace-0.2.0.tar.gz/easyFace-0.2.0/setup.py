#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import setuptools

# 供Python编程教学使用
setuptools.setup(
    name='easyFace',
    version='0.2.0',
    author='zhuzhuangtian',
    author_email='576583342@qq.com',
    url='https://github.com/zjuxumang/PyFace',
    description='fork自zxxml的PyFace项目，增加了对32bit raspbian-buster系统的支持。底层使用了yushiqi开源的libfacedetection。具体使用方法见github',
    packages=setuptools.find_packages(),
    platforms=["all"],
    python_requires='>=3.7',
    package_data={'': ['*.dll', '*.so']},
    install_requires=['numpy', 'Pillow','opencv-python']
)
