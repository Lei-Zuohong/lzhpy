# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
# Private package
# Internal package


def tanh(series: pandas.Series):
    qtp = series[series > 0].quantile(0.9)
    qtn = -series[series < 0].quantile(0.1)
    series[series > 0] = series[series > 0] / qtp
    series[series < 0] = series[series < 0] / qtn
    return numpy.tanh(series)


def inbalance_equal(value1, value2):
    return ((value1 - value2) / (value1 + value2)).significance()


def inbalance_square(num1, den1, num2, den2):
    return (num1 / den1 - num2 / den2).significance()
