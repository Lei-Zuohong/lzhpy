# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package
from .container import Line
from .unit import Unit

################################################################################
# 输出块状信息
################################################################################

config = {'line': {'loc': 'l',
                   'color': 'r'},
          'point': {'locs': ['l', 'l'],
                    'weights': [1, 2],
                    'colors': ['r', 'g']}}


def sstar():
    line = Line()
    line.add(Unit('_',
                  fill_block='_',
                  fill_length=-1,
                  style_effect='b',
                  style_front='w',
                  style_back='w'))
    return line


def sline(value):
    line = Line()
    line.add(Unit('__',
                  style_effect='b',
                  style_front='w',
                  style_back='w'))
    line.add(Unit('  '))
    line.add(Unit(value,
                  fill_loc=config['line']['loc'],
                  fill_length=-1,
                  style_effect='b',
                  style_front=config['line']['color']))
    line.add(Unit('  '))
    line.add(Unit('__',
                  style_effect='b',
                  style_front='w',
                  style_back='w'))
    return line


def spoint(value1, value2):
    line = Line()
    line.add(Unit('__',
                  style_effect='b',
                  style_front='w',
                  style_back='w'))
    line.add(Unit('  '))
    line.add(Unit(value1,
                  fill_loc=config['point']['locs'][0],
                  fill_length=-1,
                  style_effect='b',
                  style_front=config['point']['colors'][0]),
             weight=config['point']['weights'][0])
    line.add(Unit('  '))
    line.add(Unit('==>',
                  style_effect='b',
                  style_front='y'))
    line.add(Unit('  '))
    line.add(Unit(value2,
                  fill_loc=config['point']['locs'][1],
                  fill_length=-1,
                  style_effect='b',
                  style_front=config['point']['colors'][1]),
             weight=config['point']['weights'][1])
    line.add(Unit('  '))
    line.add(Unit('__',
                  style_effect='b',
                  style_front='w',
                  style_back='w'))
    return line


def pstar():
    print(sstar())


def pline(value):
    print(sline(value))


def ppoint(value1, value2):
    print(spoint(value1, value2))
