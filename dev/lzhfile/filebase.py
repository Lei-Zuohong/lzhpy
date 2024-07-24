# -*- coding: UTF-8 -*-
# Public package
import os
import numpy
import itertools
# Private package
# Internal package


class FolderTree:
    '''
    用来管理多级同结构数据库的工具
    要求数据库的目录结构为 {path_root}/{key1}/{key2}/.../
    '''

    def __init__(self, path_root, keys):
        '''
        - 通过 path_root 和 keys: [key1, key2, ...] 指定目录结构
        - {path_root}/{key1}/{key2}/.../
        '''
        self.path_root = path_root
        self.keys = keys

    def get_missing(self, *args, **argv):
        '''
        - 通过 key1=[v1,v2], key2=[v1,v2] 指定搜寻目录
        - 可选 leaf=[v1,v2] 指定目录末端文件，否则搜寻末端目录
        - 可选 axis=[...] 指定特定维度取 unique
        '''
        for key in self.keys:
            if (key not in argv):
                raise ValueError('%s should be in argv as a list' % (key))
        temp_args = []
        temp_args.append([self.path_root])
        for key in self.keys:
            temp_args.append(argv[key])
        if ('leaf' in argv):
            temp_args.append(argv['leaf'])
        prods = itertools.product(*temp_args)
        output = []
        for prod in prods:
            prod = list(prod)
            for i in range(len(prod)):
                if (type(prod[i]) in [int]):
                    prod[i] = '%d' % (prod[i])
            path = '/'.join(prod)
            if (not os.path.exists(path)):
                output.append(list(prod))
        output = numpy.array(output)
        if (output.shape[0] == 0):
            return output
        if ('axis' in argv):
            output = numpy.unique(output[:, argv['axis']], axis=0)
        return output

    def get_path(self, *args, **argv):
        '''
        - 通过 key1=v1, key2=v2 指定目录
        - 通过 输入文件名指定末端文件名，如果只指定'.csv'的格式，则默认返回名为data的文件
        '''
        for key in self.keys:
            if (key not in argv):
                raise ValueError('%s should be in argv as a object' % (key))
        output = self.path_root
        for key in self.keys:
            if (type(argv[key]) in [int]):
                output += '/%d' % (argv[key])
            else:
                output += '/%s' % (argv[key])
        if (len(args) > 0):
            if (args[0][0] == '.'):
                output += '/data%s' % (args[0])
            else:
                output += '/%s' % (args[0])
        return output
