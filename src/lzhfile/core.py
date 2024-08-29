# -*- coding: UTF-8 -*-
# Public package
import re
import os
import shutil
# Private package
# Internal package
from .types import suffix as suffix

################################################################################
# 文件系统解析
################################################################################


def isdir(path):
    return os.path.isdir(path)


def isfile(path):
    return os.path.isfile(path)


def split(path):
    '分割地址为 [文件目录，文件名]'
    output = os.path.split(path)
    return output[0], output[1]


def split_type(path):
    '分割地址为 [文件目录，文件名，文件后缀]'
    output1 = os.path.splitext(path)
    output2 = os.path.split(output1[0])
    return output2[0], output2[1], output1[1]


def split_drive(path):
    '分割地址为 [磁盘符，后续路径]'
    output = os.path.splitdrive(path)
    return output[0], output[1]


def join(*args):
    return os.path.join(*args)


def get_size_file(path):
    '返回文件大小'
    return os.path.getsize(path)


def _size_trans(size):
    '转换文件大小为字符串'
    uni = 1024
    if size < uni:
        size = '%i' % size + ' B'
    elif uni <= size < uni**2:
        size = '%.2f' % float(size / uni) + ' KB'
    elif uni**2 <= size < uni**3:
        size = '%.2f' % float(size / uni**2) + ' MB'
    elif uni**3 <= size < uni**4:
        size = '%.2f' % float(size / uni**3) + ' GB'
    elif uni**4 <= size:
        size = '%.2f' % float(size / uni**4) + ' TB'
    return size

################################################################################
# 文件系统操作
################################################################################


def mv(path_source, path_target):
    shutil.move(path_source, path_target)


def rm(path):
    if (os.path.isdir(path)):
        shutil.rmtree(path)
    elif (os.path.exists(path)):
        os.remove(path)


def makedirs(path):
    os.makedirs(path, exist_ok=True)


def copy_file(source='', target=''):
    source_path, source_name = split(source)
    target_path, target_name = split(target)
    if (target_name in os.listdir(target_path)):
        os.remove('%s/%s' % (target_path, target_name))
    shutil.copy('%s/%s' % (source_path, source_name),
                '%s' % (target_path))
    if (source_name != target_name):
        shutil.move('%s/%s' % (target_path, source_name),
                    '%s/%s' % (target_path, target_name))


def copy_folder(source='', target='', delete_origin=True):
    source_path, source_name = split(source)
    target_path, target_name = split(target)
    if (delete_origin):
        if (target_name in os.listdir(target_path)):
            shutil.rmtree('%s/%s' % (target_path, target_name))
    shutil.copytree('%s/%s' % (source_path, source_name),
                    '%s/%s' % (target_path, target_name))


def copy(source='', target=''):
    if (os.path.isfile(source)):
        copy_file(source, target)
    else:
        copy_folder(source, target)

################################################################################
# 资源管理器
################################################################################


class File:
    def __init__(self, path):
        if (not os.path.isfile(path)):
            raise Exception("This is not a file: %s" % (path))
        self.path = path
        self.name = split(path)[-1]
        self.type = split_type(path)[-1]
        self.size = get_size_file(path)

    def get_size(self, string=False):
        if (string):
            return _size_trans(self.size)
        else:
            return self.size

    def is_video(self):
        return self.type in suffix.video

    def is_picture(self):
        return self.type in suffix.picture


class Folder:
    def __init__(self, path):
        if (not os.path.isdir(path)):
            raise Exception("This is not a folder: %s" % (path))
        self.tree = self._get_tree(path)
        self.leaf = self._get_leaf(path)

    def _get_tree(self, path):
        output = {}
        if (os.path.isfile(path)):
            return File(path)
        else:
            files = os.listdir(path)
            for file in files:
                if (re.match(r'\.(.*)', file)):
                    continue
                output[file] = self._get_tree(os.path.join(path, file))
            return output

    def _get_leaf(self, path):
        output = []
        if (os.path.isfile(path)):
            output.append(File(path))
        else:
            files = os.listdir(path)
            for file in files:
                if (re.match(r'\.(.*)', file)):
                    continue
                output += self._get_leaf(os.path.join(path, file))
        return output

    def get_size(self, string=False):
        size = 0
        for file in self.leaf:
            size += file.size
        if (string):
            size = _size_trans(size)
        return size

    def get_videos(self):
        output = [leaf for leaf in self.leaf if leaf.is_video()]
        return output

    def get_pictures(self):
        output = [leaf for leaf in self.leaf if leaf.is_picture()]
        return output
