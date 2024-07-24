# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package
from ..core import *


def txt_write(filename, out_string, encoding='utf-8'):
    '输出字符串到txt文件'
    if (split(filename)[0] != ''):
        makedirs(split(filename)[0])
    with open(filename, 'w', encoding=encoding) as outfile:
        outfile.write(out_string)


def txt_writelines(filename, out_strings, encoding='utf-8'):
    '输出字符串列表到txt文件'
    if (split(filename)[0] != ''):
        makedirs(split(filename)[0])
    output = ''
    for out_string in out_strings:
        output += out_string
        output += '\n'
    txt_write(filename, output, encoding=encoding)


def txt_read(filename, encoding='utf-8'):
    '读取文件为string'
    with open(filename, 'r', encoding=encoding) as infile:
        output = infile.read()
    return output


def txt_readlines(filename, encoding='utf-8'):
    '读取文件为string列表'
    with open(filename, 'r', encoding=encoding) as infile:
        output = infile.readlines()
    for i in range(len(output)):
        output[i] = output[i][:-1]
    return output


def txt_add(filename, out_string, encoding='utf-8'):
    output = txt_read(filename)
    output += out_string
    txt_write(filename, output, encoding=encoding)
