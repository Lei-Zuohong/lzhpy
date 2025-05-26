# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package


def fit(x, y):
    mean_x = x.mean()
    mean_y = y.mean()
    eps_x = x - mean_x
    eps_y = y - mean_y
    beta = (eps_y * eps_x).sum() / (eps_x**2).sum()
    alpha = mean_y - mean_x * beta
    r = (eps_y * eps_x).sum() / numpy.sqrt((eps_x**2).sum()) / numpy.sqrt((eps_y**2).sum())

    yp = x * beta + alpha
    eps_yp = yp - yp.mean()
    eps = y - yp
    sse = (eps**2).sum()
    ssr = (eps_yp**2).sum()
    sst = (eps_y**2).sum()
    beta_e = numpy.sqrt(((eps**2).sum()) / ((eps_x**2).sum()) / (len(x) - 2))
    alpha_e = beta_e * numpy.sqrt(numpy.sum(x**2) / len(x))
    if (beta_e == 0):
        beta_t = numpy.inf
    else:
        beta_t = beta / beta_e
    alpha_t = alpha / alpha_e
    r2 = ssr / sst

    return [beta, alpha, r,
            eps_x, eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e, alpha_e,
            beta_t, alpha_t,
            r2]


def fitw(x, y, w):
    mean_x = (x * w).sum() / w.sum()
    mean_y = (y * w).sum() / w.sum()
    eps_x = x - mean_x
    eps_y = y - mean_y
    beta = (eps_y * eps_x * w).sum() / (eps_x**2 * w).sum()
    alpha = mean_y - mean_x * beta
    r = (eps_y * eps_x * w).sum() / numpy.sqrt((eps_x**2 * w).sum()) / numpy.sqrt((eps_y**2 * w).sum())

    yp = x * beta + alpha
    eps_yp = yp - (yp * w).sum() / w.sum()
    eps = y - yp
    sse = (eps**2 * w).sum()
    ssr = (eps_yp**2 * w).sum()
    sst = (eps_y**2 * w).sum()
    beta_e = numpy.sqrt(((eps**2 * w).sum()) / ((eps_x**2 * w).sum()) / (len(x) - 2))
    alpha_e = beta_e * numpy.sqrt(numpy.sum(x**2 * w) / len(x))
    if (beta_e == 0):
        beta_t = numpy.inf
    else:
        beta_t = beta / beta_e
    alpha_t = alpha / alpha_e
    r2 = ssr / sst

    return [beta, alpha, r,
            eps_x, eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e, alpha_e,
            beta_t, alpha_t,
            r2]
