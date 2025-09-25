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


def tanh(series: pandas.Series):
    output = series.copy()
    output[numpy.isnan(output)] = 0
    qtp = output[output > 0].quantile(0.9)
    qtn = -output[output < 0].quantile(0.1)
    output[output > 0] = output[output > 0] / qtp
    output[output < 0] = output[output < 0] / qtn
    return numpy.tanh(output)


def standardize(series: pandas.Series):
    output = series.copy()
    output[numpy.isnan(output)] = 0
    output[output > output.quantile(0.99)] = output.quantile(0.99)
    output[output < output.quantile(0.01)] = output.quantile(0.01)
    output = (output - output.mean()) / output.std() / 3
    output[output > 1] = 1
    output[output < -1] = -1
    return output
