# -*- coding: UTF-8 -*-
# Public package
import re
import os
# Private package
# Internal package
from .path import *
from .operate import *


def get_size_file(path):  # 返回文件大小
    return os.path.getsize(path)


def _size_trans(size):  # 转换文件大小为字符串
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


suffix = {'video': ['.mkv', '.MKV', '.avi', '.AVI', '.wmv', '.WMV',
                    '.mpeg', '.MPEG', '.mov', '.MOV', '.rm', '.RM',
                    '.ram', '.RAM', '.flv', '.FLV', '.mp4', '.MP4',
                    '.rmvb', '.RMVB'],
          'picture': ['.jpg', '.jpeg', '.png']}


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
        return self.type in suffix['video']

    def is_picture(self):
        return self.type in suffix['picture']


class Folder:
    def __init__(self, path):
        if (not os.path.isdir(path)):
            raise Exception("This is not a folder: %s" % (path))
        self.tree = self.__get_tree(path)
        self.leaf = self.__get_leaf(path)

    def __get_tree(self, path):
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

    def __get_leaf(self, path):
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
