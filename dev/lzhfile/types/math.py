# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package


def memmap_write(filename, objout, dtype='float32'):
    numpy.memmap(filename, dtype=dtype, mode='w+', shape=objout.shape)[...] = objout
    return None


def memmap_read(filename, dtype='float32', reshape=[-1]):
    output = numpy.memmap(filename, dtype=dtype, mode='r').reshape(*reshape)
    return output
