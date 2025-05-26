# -*- coding: UTF-8 -*-
# Public package
import numpy
import lmfit
# Private package
# Internal package
from .utils import *


def residual(ps, y, x):
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    return output


def residual_weight(ps, y, x, w):
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    output *= w
    return output


def fit(x, y, hint=None):
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

    return [beta, r,
            eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e,
            beta_t,
            r2]


def fitw(x, y, w, hint=None):
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

    return [beta, r,
            eps_y, eps_yp, eps,
            sse, ssr, sst,
            beta_e,
            beta_t,
            r2]
