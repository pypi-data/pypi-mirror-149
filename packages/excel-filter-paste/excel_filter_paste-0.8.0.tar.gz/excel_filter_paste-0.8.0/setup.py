#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from setuptools import setup, find_packages


setup(
    name="excel_filter_paste",
    version="0.8.0",
    install_requires=[
        "openpyxl",
        "pandas",
        "click",
    ],
    packages=["excel_filter_paste"],
    entry_points={
        "console_scripts": [
            'excel_filter_paste=excel_filter_paste.__main__:run',
            'paste=excel_filter_paste.__main__:paste',
        ],
    },
)
