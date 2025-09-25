# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
# Private package
# Internal package
import lzhmath.lzhreg as lzhreg


def fac_from_v(array: numpy.ndarray) -> pandas.Series:
    y = array[(~numpy.isnan(array)) & (~numpy.isinf(array))]
    if (y.shape[0] > 1):
        mean = numpy.mean(y)
        var = numpy.sum((y - numpy.mean(y))**2) / (y.shape[0] - 1)
        skew = numpy.sum((y - numpy.mean(y))**3) / var**1.5 / y.shape[0]
        kurt = numpy.sum((y - numpy.mean(y))**4) / var**2 / y.shape[0] - 3
        return pandas.Series({'mean': mean, 'var': var, 'skew': skew, 'kurt': kurt})
    else:
        return pandas.Series(numpy.nan, index=['mean', 'var', 'skew', 'kurt'])


def reg_vt(array: numpy.ndarray) -> pandas.Series:
    reg = lzhreg.Linear(array, numpy.arange(array.shape[0]))
    if (reg.clean()):
        reg.fit()
        last = reg.y[-1] - reg.x[-1] * reg.result.beta - reg.result.alpha
        last_e = ((reg.x[-1] * reg.result.beta_e)**2 + (reg.result.alpha_e)**2)**0.5
        last_t = last / last_e
        residual = array - numpy.arange(array.shape[0]) * reg.result.beta - reg.result.alpha
        return pandas.Series({'alpha': reg.result.alpha,
                              'alpha_t': reg.result.alpha_t,
                              'beta': reg.result.beta,
                              'beta_t': reg.result.beta_t,
                              'r': reg.result.r,
                              'last_t': last_t}), residual
    else:
        return pandas.Series(numpy.nan, index=['alpha',
                                               'alpha_t',
                                               'beta',
                                               'beta_t',
                                               'r',
                                               'last_t']), array


def fac_from_vt(array: numpy.ndarray) -> pandas.Series:
    output1, residual = reg_vt(array)
    output2 = fac_from_v(residual)
    return pandas.concat([output1, output2])


def reg_vv(array1: numpy.ndarray, array2: numpy.ndarray) -> pandas.Series:
    reg = lzhreg.Linear(array1, array2)
    if (reg.clean()):
        reg.fit()
        last = reg.y[-1] - reg.x[-1] * reg.result.beta - reg.result.alpha
        last_e = ((reg.x[-1] * reg.result.beta_e)**2 + (reg.result.alpha_e)**2)**0.5
        last_t = last / last_e
        residual = array1 - array2 * reg.result.beta - reg.result.alpha
        return pandas.Series({'alpha': reg.result.alpha,
                              'alpha_t': reg.result.alpha_t,
                              'beta': reg.result.beta,
                              'beta_t': reg.result.beta_t,
                              'r': reg.result.r,
                              'last_t': last_t}), residual
    else:
        return pandas.Series(numpy.nan, index=['alpha',
                                               'alpha_t',
                                               'beta',
                                               'beta_t',
                                               'r',
                                               'last_t']), array1


def fac_from_vv(array1: numpy.ndarray, array2: numpy.ndarray) -> pandas.Series:
    output1, residual = reg_vv(array1, array2)
    output2 = fac_from_v(residual)
    return pandas.concat([output1, output2])


def fac_from_vvt(array1: numpy.ndarray, array2: numpy.ndarray) -> pandas.Series:
    _, residual = reg_vv(array1, array2)
    return fac_from_vt(residual)
