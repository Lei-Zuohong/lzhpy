# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package
from .unit import Unit
from .container import Line


def hori():
    line = Line()
    line.add(Unit('|'))
    line.add(Unit('',
                  fill_block='-',
                  fill_length=-1))
    line.add(Unit('|'))
    return line
