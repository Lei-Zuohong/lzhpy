# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
# Private package
# Internal package
import lzhsta.regress as regress


def fac_from_v(array):
    y = array[(~numpy.isnan(array)) & (~numpy.isinf(array))]
    if (y.shape[0] > 1):
        mean = numpy.mean(y)
        var = numpy.sum((y - numpy.mean(y))**2) / (y.shape[0] - 1)
        skew = numpy.sum((y - numpy.mean(y))**3) / var**1.5 / y.shape[0]
        kurt = numpy.sum((y - numpy.mean(y))**4) / var**2 / y.shape[0]
        return pandas.Series({'mean': mean, 'var': var, 'skew': skew, 'kurt': kurt})
    else:
        return pandas.Series(numpy.nan, index=['mean', 'var', 'skew', 'kurt'])


def reg_vt(array):
    reg = regress.Linear(array, numpy.arange(array.shape[0]))
    if (reg.clean()):
        reg.fit()
        last = reg.y[-1] - reg.x[-1] * reg.beta - reg.alpha
        last_e = ((reg.x[-1] * reg.beta_e)**2 + (reg.alpha_e)**2)**0.5
        last_t = last / last_e
        residual = array - numpy.arange(array.shape[0]) * reg.beta - reg.alpha
        return pandas.Series({'alpha': reg.alpha,
                              'alpha_t': reg.alpha_t,
                              'beta': reg.beta,
                              'beta_t': reg.beta_t,
                              'r': reg.r,
                              'last': last_t}), residual
    else:
        return pandas.Series(numpy.nan, index=['alpha',
                                               'alpha_t',
                                               'beta',
                                               'beta_t',
                                               'r',
                                               'last']), array


def fac_from_vt(array):
    output1, residual = reg_vt(array)
    output2 = fac_from_v(residual)
    return pandas.concat([output1, output2])


def reg_vv(array1, array2):
    reg = regress.Linear(array1, array2)
    if (reg.clean()):
        reg.fit()
        last = reg.y[-1] - reg.x[-1] * reg.beta - reg.alpha
        last_e = ((reg.x[-1] * reg.beta_e)**2 + (reg.alpha_e)**2)**0.5
        last_t = last / last_e
        residual = array2 - array1 * reg.beta - reg.alpha
        return pandas.Series({'alpha': reg.alpha,
                              'alpha_t': reg.alpha_t,
                              'beta': reg.beta,
                              'beta_t': reg.beta_t,
                              'r': reg.r,
                              'last': last_t}), residual
    else:
        return pandas.Series(numpy.nan, index=['alpha',
                                               'alpha_t',
                                               'beta',
                                               'beta_t',
                                               'r',
                                               'last']), array2


def fac_from_vv(array1, array2):
    output1, residual = reg_vv(array1, array2)
    output2 = fac_from_v(residual)
    return pandas.concat([output1, output2])


def fac_from_vvt(array1, array2):
    _, residual = reg_vv(array1, array2)
    return fac_from_vt(residual)
