# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package
from .utils import *


def fit(x, y, stable=False):
    match(stable):
        case(True):
            temp_inv = inverse_matrix(x  @ x.T)
        case(False):
            temp_inv = numpy.linalg.inv(x  @ x.T)
    beta = temp_inv @ x @  y
    yp = beta @ x
    eps_yp = yp - yp.mean()
    eps_y = y - y.mean()
    eps = y - yp
    sse = ((eps)**2).sum()
    ssr = ((eps_yp)**2).sum()
    sst = ((eps_y)**2).sum()
    mse = ((eps)**2).mean()
    temp = mse * temp_inv * x.shape[1] / (x.shape[1] - x.shape[0])
    temp[numpy.where(temp < 0)] = 0.0
    beta_e = numpy.diagonal(numpy.sqrt(temp))
    beta_t = beta / beta_e
    r2 = ssr / sst
    r = numpy.sqrt(r2)

    return [beta, r,
            eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e,
            beta_t,
            r2]


def fitw(x, y, w, stable=False):
    match(stable):
        case(True):
            temp_inv = inverse_matrix(x @ numpy.diag(w) @ x.T)
        case(False):
            temp_inv = numpy.linalg.inv(x @ numpy.diag(w) @ x.T)
    beta = temp_inv @ x @ numpy.diag(w) @ y
    yp = beta @ x
    eps_yp = yp - (yp * w).sum() / w.sum()
    eps_y = y - (y * w).sum() / w.sum()
    eps = y - yp
    sse = ((eps)**2 * w).sum()
    ssr = ((eps_yp)**2 * w).sum()
    sst = ((eps_y)**2 * w).sum()
    mse = ((eps)**2 * w).sum() / w.sum()
    temp = mse * temp_inv * x.shape[0] / (x.shape[0] - x.shape[1])
    temp[numpy.where(temp < 0)] = 0.0
    beta_e = numpy.diagonal(numpy.sqrt(temp))
    beta_t = beta / beta_e
    r2 = ssr / sst
    r = numpy.sqrt(r2)

    return [beta, r,
            eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e,
            beta_t,
            r2]
