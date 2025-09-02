# -*- coding: UTF-8 -*-
# Public package
import os
# Private package
# Internal package


def isdir(path):
    return os.path.isdir(path)


def isfile(path):
    return os.path.isfile(path)


def split(path):  # 分割地址为 [文件目录，文件名]
    return os.path.split(path)


def split_type(path):  # 分割地址为 [文件目录，文件名，文件后缀]
    presuffix, suffix = os.path.splitext(path)
    folder, file = os.path.split(presuffix)
    return folder, file, suffix


def split_drive(path):  # 分割地址为 [磁盘符，后续路径]
    return os.path.splitdrive(path)


def join(*args):  # 拼接路径
    return os.path.join(*args)
