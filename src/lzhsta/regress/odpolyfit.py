# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package


def fit(x, y):
    para, cova = numpy.polyfit(x, y, 1, cov=True)
    beta = para[0]
    alpha = para[1]
    beta_e = numpy.sqrt(cova[0][0])
    alpha_e = numpy.sqrt(cova[1][1])
    beta_t = beta / beta_e
    alpha_t = alpha / alpha_e
    return [beta, alpha,
            beta_e, alpha_e,
            beta_t, alpha_t]


def fitw(x, y, w):
    para, cova = numpy.polyfit(x, y, 1, w=w, cov=True)
    beta = para[0]
    alpha = para[1]
    beta_e = numpy.sqrt(cova[0][0])
    alpha_e = numpy.sqrt(cova[1][1])
    beta_t = beta / beta_e
    alpha_t = alpha / alpha_e
    return [beta, alpha,
            beta_e, alpha_e,
            beta_t, alpha_t]
