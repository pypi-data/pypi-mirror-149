#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import click
import logging
from pathlib import Path

from excel_filter_paste.base import convert
from excel_filter_paste.paste import paste_convert


logger = logging.getLogger("excel_filter_paste")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--input", prompt="输入需要转化的文件路径", help="输入需要转化的文件路径(如: D:/原始文件.xlsx)")
@click.option("--output", prompt="输入转化后文件的保存路径", help="输入转化后文件的保存路径(如: D:/结果.xlsx)")
@click.option("--directory", prompt="输入文件夹", help="输入文件夹(如: D:/test)")
def paste(input, output, directory):
    paste_convert(input, output, directory)


@cli.command()
@click.option("--input", prompt="输入需要转化的文件路径", help="输入需要转化的文件路径(如: D:/原始文件.xlsx)")
@click.option("--output", prompt="输入转化后文件的保存路径", help="输入转化后文件的保存路径(如: D:/结果.xlsx)")
@click.option("--from-column", prompt="输入需要复制的列", help="输入需要复制的列(如: C)")
@click.option("--to-column", prompt="输入需要粘贴的列", help="输入需要粘贴的列(如: B)")
def run(input, output, from_column, to_column):
    convert(input, output, from_column, to_column)


if __name__ == "__main__":
    cli()
