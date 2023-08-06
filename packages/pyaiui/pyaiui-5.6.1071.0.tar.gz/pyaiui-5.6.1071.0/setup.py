# -*- coding: utf-8 -*-

import os
import setuptools
import platform


with open("README.txt", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaiui",
    version="5.6.1071.0",
    author="zrmei",
    author_email="zrmei@iflytek.com",
    description="aiui sdk for python.",
    long_description=long_description,
    url="https://aiui.xfyun.cn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    data_files=[
        ("pyaiui/libs/ELF/64bit", ["pyaiui/libs/ELF/64bit/libaiui.so"]),
        ("pyaiui/libs/ELF/32bit", ["pyaiui/libs/ELF/32bit/libaiui.so"]),
        ("pyaiui/libs/WindowsPE/64bit", ["pyaiui/libs/WindowsPE/64bit/libaiui.so"]),
        ("pyaiui/libs/WindowsPE/32bit", ["pyaiui/libs/WindowsPE/32bit/libaiui.so"]),
    ]
)
