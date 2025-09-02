# -*- coding: UTF-8 -*-
# Public package
import numpy
import lmfit
# Private package
# Internal package
from .tools import *


def residual(ps: lmfit.Parameters,
             y: numpy.ndarray,
             x: numpy.ndarray) -> numpy.ndarray:
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    return output


def residual_weight(ps: lmfit.Parameters,
                    y: numpy.ndarray,
                    x: numpy.ndarray,
                    w: numpy.ndarray) -> numpy.ndarray:
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    output *= w
    return output


def fit(x: numpy.ndarray,
        y: numpy.ndarray,
        hint: numpy.ndarray = None) -> FitResult:
    ps = lmfit.Parameters()
    for i in range(x.shape[0]):
        if (hint is not None):
            ps.add(name='beta%d' % (i), value=hint[i][0], min=hint[i][1], max=hint[i][2])
        else:
            ps.add(name='beta%d' % (i), value=0.0, min=-10000, max=10000)
    result = lmfit.minimize(residual, params=ps, method='leastsq', args=(y, x))
    # lmfit.printfuncs.report_fit(result.params, min_correl=0.5)
    beta_ = []
    betae_ = []
    for i in range(x.shape[0]):
        beta_.append(result.params['beta%d' % (i)].value)
        if (None is not result.params['beta%d' % (i)].stderr):
            betae_.append(result.params['beta%d' % (i)].stderr)
        else:
            betae_.append(result.params['beta%d' % (i)].value)
    beta = numpy.array(beta_)
    beta_e = numpy.array(betae_)
    beta_t = beta / beta_e

    yp = beta @ x
    eps_yp = yp - yp.mean()
    eps_y = y - y.mean()
    eps = y - yp
    sse = ((eps)**2).sum()
    ssr = ((eps_yp)**2).sum()
    sst = ((eps_y)**2).sum()
    r2 = ssr / sst
    r = numpy.sqrt(r2)

    result = FitResult()
    result.beta = beta
    result.beta_e = beta_e
    result.beta_t = beta_t
    result.r = r
    result.r2 = r2
    result.eps_yp = eps_yp
    result.eps = eps
    result.sse = sse
    result.ssr = ssr
    result.sst = sst
    return result


def fitw(x: numpy.ndarray,
         y: numpy.ndarray,
         w: numpy.ndarray,
         hint: numpy.ndarray = None) -> FitResult:
    ps = lmfit.Parameters()
    for i in range(x.shape[0]):
        if (hint is not None):
            ps.add(name='beta%d' % (i), value=hint[i][0], min=hint[i][1], max=hint[i][2])
        else:
            ps.add(name='beta%d' % (i), value=0.0, min=-10000, max=10000)
    result = lmfit.minimize(residual_weight, params=ps, method='leastsq', args=(y, x, w))
    # lmfit.printfuncs.report_fit(result.params, min_correl=0.5)
    beta_ = []
    betae_ = []
    for i in range(x.shape[0]):
        beta_.append(result.params['beta%d' % (i)].value)
        if (None is not result.params['beta%d' % (i)].stderr):
            betae_.append(result.params['beta%d' % (i)].stderr)
        else:
            betae_.append(result.params['beta%d' % (i)].value)
    beta = numpy.array(beta_)
    beta_e = numpy.array(betae_)
    beta_t = beta / beta_e

    yp = beta @ x
    eps_yp = yp - (yp * w).sum() / w.sum()
    eps_y = y - (y * w).sum() / w.sum()
    eps = y - yp
    sse = ((eps)**2 * w).sum()
    ssr = ((eps_yp)**2 * w).sum()
    sst = ((eps_y)**2 * w).sum()
    r2 = ssr / sst
    r = numpy.sqrt(r2)

    result = FitResult()
    result.beta = beta
    result.beta_e = beta_e
    result.beta_t = beta_t
    result.r = r
    result.r2 = r2
    result.eps_yp = eps_yp
    result.eps = eps
    result.sse = sse
    result.ssr = ssr
    result.sst = sst
    return result
