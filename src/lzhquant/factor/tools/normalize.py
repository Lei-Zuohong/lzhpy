# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
# Private package
# Internal package


def normalize(array, clip=None, scale=None, central=False):
    output = array.copy()
    if (clip is not None):
        qtl, qtr = numpy.nanquantile(output, [clip, (1 - clip)])
        output = numpy.clip(output, qtl, qtr)
    if (central):
        mean = numpy.nanmean(output)
        output = output - mean
    if (scale is not None):
        std = numpy.nanstd(output)
        output = output / std / scale
    return output
