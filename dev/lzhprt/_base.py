# -*- coding: UTF-8 -*-
# Public package
import math
import numpy
# Private package
# Internal package

################################################################################
# 定义各种数据类型到字符的转换方式
################################################################################


class Base:
    '''提供数据类型的基本接口

    Methods:
        __init__: 初始化数据类型，接受关键字列表
        __repr__: 将数据类型转换为字符串
        types: 返回该数据类型的所有支持类型
    '''

    def __init__(self, value, **argv):
        self.value = value

    def __repr__(self):
        return self.value

    @staticmethod
    def types():
        return []


class Str(Base):
    @staticmethod
    def types():
        return [str]

    def __init__(self, value, **argv):
        self.value = value

    def __repr__(self):
        return self.value


class Int(Base):
    @staticmethod
    def types():
        return [int, numpy.int16, numpy.int32, numpy.int64]

    def __init__(self, value, **argv):
        '''
        Argv:
            value_length: (int): lenth of output string
        '''
        self.value = value
        if ('value_length' in argv):
            self.length = argv['value_length']
        else:
            self.length = None

    def __repr__(self):
        if (self.length is None):
            return str(self.value)
        else:
            return str(self.value).zfill(self.length)


class Float(Base):
    @staticmethod
    def types():
        return [float, numpy.float16, numpy.float32, numpy.float64]

    def __init__(self, value, **argv):
        '''
        Argv:
            value_length: (int): lenth of output string
            value_inpercent: (bool): whether format in percentage
        '''
        self.value = value
        if ('value_length' in argv):
            self.length = argv['value_length']
        else:
            self.length = None
        # whether format in percentage
        if ('value_inpercent' in argv and argv['value_inpercent'] == True):
            self.inpercent = True
        else:
            self.inpercent = False

    def float_fix(self, value, length):
        'format float value to string with fixed length'
        return max(0, min(length - 2, length - 2 - int(math.log10(abs(value))))) if value else length - 2

    def __repr__(self):
        if (self.inpercent):
            if (self.length is None):
                return str(self.value * 100) + '%%'
            else:
                return '%.*f%%' % (self.float_fix(self.value * 100, self.length - 1), self.value * 100)
        else:
            if (self.length is None):
                return str(self.value)
            else:
                return '%.*f' % (self.float_fix(self.value, self.length), self.value)
