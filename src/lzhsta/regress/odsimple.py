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
    return [beta, alpha, r,
            eps_x, eps_y]


def fitw(x, y, w):
    mean_x = (x * w).sum() / w.sum()
    mean_y = (y * w).sum() / w.sum()
    eps_x = x - mean_x
    eps_y = y - mean_y
    beta = (eps_y * eps_x * w).sum() / (eps_x**2 * w).sum()
    alpha = mean_y - mean_x * beta
    r = (eps_y * eps_x * w).sum() / numpy.sqrt((eps_x**2 * w).sum()) / numpy.sqrt((eps_y**2 * w).sum())
    return [beta, alpha, r,
            eps_x, eps_y]