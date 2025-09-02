# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package
from .tools import *


def fit(x: numpy.ndarray,
        y: numpy.ndarray) -> FitResult:
    para, cova = numpy.polyfit(x, y, 1, cov=True)
    beta = para[0]
    alpha = para[1]
    beta_e = numpy.sqrt(cova[0][0])
    alpha_e = numpy.sqrt(cova[1][1])
    beta_t = beta / beta_e
    alpha_t = alpha / alpha_e

    result = FitResult()
    result.beta = beta
    result.alpha = alpha
    result.beta_e = beta_e
    result.beta_t = beta_t
    result.alpha_e = alpha_e
    result.alpha_t = alpha_t
    return result


def fitw(x: numpy.ndarray,
         y: numpy.ndarray,
         w: numpy.ndarray) -> FitResult:
    para, cova = numpy.polyfit(x, y, 1, w=w, cov=True)
    beta = para[0]
    alpha = para[1]
    beta_e = numpy.sqrt(cova[0][0])
    alpha_e = numpy.sqrt(cova[1][1])
    beta_t = beta / beta_e
    alpha_t = alpha / alpha_e

    result = FitResult()
    result.beta = beta
    result.alpha = alpha
    result.beta_e = beta_e
    result.beta_t = beta_t
    result.alpha_e = alpha_e
    result.alpha_t = alpha_t
    return result
