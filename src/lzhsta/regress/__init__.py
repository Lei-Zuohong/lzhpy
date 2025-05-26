# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package
from .utils import *
from . import odsimple as odsimple
from . import odlinear as odlinear
from . import odpolyfit as odpolyfit
from . import tdlinear as tdlinear
from . import tdlmfit as tdlmfit


class Linear():
    def __init__(self, y, x, w=None):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is not None):
            self.w = to_ndarray(w)
        self.method = 'linear'
        self.drop_nan = True  # 是否删除nan
        self.drop_inf = True  # 是否删除inf
        self.drop_zero = False  # 是否删除0

    def clean(self):
        # 筛选有效数据
        index = numpy.ones(self.y.shape[0], dtype=bool)
        if (self.drop_nan):
            for array in [self.y, self.x]:
                index &= ~numpy.isnan(array)
        if (self.drop_inf):
            for array in [self.y, self.x]:
                index &= ~numpy.isinf(array)
        if (self.drop_zero):
            for array in [self.y, self.x]:
                index &= array != 0
        if (hasattr(self, 'w')):
            index &= ~numpy.isnan(self.w)
            index &= ~numpy.isinf(self.w)
            index &= self.w != 0
        # 重构数据
        self.y = self.y[index]
        self.x = self.x[index]
        if (hasattr(self, 'w')):
            self.w = self.w[index]
        # 返回结果
        if (self.y.shape[0] > 2):
            return True
        else:
            return False

    def fit(self):
        match(self.method):
            case('simple'):
                self.__fit_simple()
            case('linear'):
                self.__fit_linear()
            case('polyfit'):
                self.__fit_polyfit()
            case _:
                raise ValueError('method not support')

    def __fit_simple(self):
        if (hasattr(self, 'w')):
            [self.beta, self.alpha, self.r,
             self.eps_x, self.eps_y] = odsimple.fitw(self.x, self.y, self.w)
        else:
            [self.beta, self.alpha, self.r,
             self.eps_x, self.eps_y] = odsimple.fit(self.x, self.y)

    def __fit_linear(self):
        if (hasattr(self, 'w')):
            [self.beta, self.alpha, self.r,
             self.eps_x, self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             self.beta_e, self.alpha_e,
             self.beta_t, self.alpha_t,
             self.r] = odlinear.fitw(self.x, self.y, self.w)
        else:
            [self.beta, self.alpha, self.r,
             self.eps_x, self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             self.beta_e, self.alpha_e,
             self.beta_t, self.alpha_t,
             self.r] = odlinear.fit(self.x, self.y)

    def __fit_polyfit(self):
        if (hasattr(self, 'w')):
            [self.beta, self.alpha,
             self.beta_e, self.alpha_e,
             self.beta_t, self.alpha_t] = odpolyfit.fitw(self.x, self.y, self.w)
        else:
            [self.beta, self.alpha,
             self.beta_e, self.alpha_e,
             self.beta_t, self.alpha_t] = odpolyfit.fit(self.x, self.y)


class MultiLinear():
    def __init__(self, y, x, w=None, stable=False):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is not None):
            self.w = to_ndarray(w)
        self.method = 'linear'
        self.force_neutral = False
        self.drop_nan = True
        self.drop_inf = True
        self.drop_zero = False
        self.stable = stable

    def clean(self):
        index = numpy.ones(self.y.shape[0], dtype=bool)
        if (self.drop_nan):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= ~numpy.isnan(array)
        if (self.drop_inf):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= ~numpy.isinf(array)
        if (self.drop_zero):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= array != 0
        if (hasattr(self, 'w')):
            index &= ~numpy.isnan(self.w)
            index &= ~numpy.isinf(self.w)
            index &= self.w != 0
        self.y = self.y[index]
        self.x = self.x[:, index]
        if (hasattr(self, 'w')):
            self.w = self.w[index]
        if (self.y.shape[0] > self.x.shape[0]):
            return True
        else:
            return False

    def fit(self):
        match(self.method):
            case('linear'):
                self.__fit_linear()
            case('lmfit'):
                self.__fit_lmfit()
            case _:
                raise ValueError('method not support')

    def __fit_linear(self):
        if (self.force_neutral):
            ix = self.x
        else:
            ix = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0)

        if (hasattr(self, 'w')):
            [beta, self.r,
             self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             beta_e,
             beta_t,
             self.r2] = tdlinear.fitw(ix, self.y, self.w, stable=self.stable)
        else:
            [beta, self.r,
             self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             beta_e,
             beta_t,
             self.r2] = tdlinear.fit(ix, self.y, stable=self.stable)

        if (self.force_neutral):
            self.beta = beta
            self.beta_e = beta_e
            self.beta_t = beta_t
            self.alpha = 0.0
            self.alpha_e = 0.0
            self.alpha_t = 0.0
        else:
            self.beta = beta[:-1]
            self.beta_e = beta_e[:-1]
            self.beta_t = beta_t[:-1]
            self.alpha = beta[-1]
            self.alpha_e = beta_e[-1]
            self.alpha_t = beta_t[-1]

    def __fit_lmfit(self):
        if (self.force_neutral):
            ix = self.x
        else:
            ix = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0)

        if (hasattr(self, 'w')):
            [beta, self.r,
             self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             beta_e,
             beta_t,
             self.r2] = tdlmfit.fitw(ix, self.y, self.w)
        else:
            [beta, self.r,
             self.eps_y, self.eps_yp, self.eps,
             self.sse, self.ssr, self.sst,
             beta_e,
             beta_t,
             self.r2] = tdlmfit.fit(ix, self.y)

        if (self.force_neutral):
            self.beta = beta
            self.beta_e = beta_e
            self.beta_t = beta_t
            self.alpha = 0.0
            self.alpha_e = 0.0
            self.alpha_t = 0.0
        else:
            self.beta = beta[:-1]
            self.beta_e = beta_e[:-1]
            self.beta_t = beta_t[:-1]
            self.alpha = beta[-1]
            self.alpha_e = beta_e[-1]
            self.alpha_t = beta_t[-1]
