#pragma once
#include <cmath>
#include <stdexcept>
#include "typedef.hpp"

// oid: 0   =>   out: r
// oid: 1   =>   out: alpha
// oid: 2   =>   out: beta
// oid: 11  =>   out: alpha_e
// oid: 12  =>   out: alpha_t
// oid: 21  =>   out: beta_e
// oid: 22  =>   out: beta_t

double regression_linear(Vdouble x, Vdouble y, int oid)
{
    int n = x.size();
    // mean
    double meanx = 0;
    double meany = 0;
    for (int i = 0; i < n; ++i)
    {
        meanx += x[i];
        meany += y[i];
    }
    meanx /= n;
    meany /= n;
    // epsilon
    double epsx = 0;
    double epsy = 0;
    double epsxy = 0;
    for (int i = 0; i < n; ++i)
    {
        epsx += (x[i] - meanx) * (x[i] - meanx);
        epsy += (y[i] - meany) * (y[i] - meany);
        epsxy += (x[i] - meanx) * (y[i] - meany);
    }
    if (epsx == 0 || epsy == 0)
    {
        return std::nan("1");
    }
    // id 0, 1, 2
    switch (oid)
    {
    case (0):
    {
        return epsxy / sqrt(epsx * epsy);
        break;
    }
    case (1):
    {
        return meany - epsxy / epsx * meanx;
        break;
    }
    case (2):
    {
        return epsxy / epsx;
        break;
    }
    }
    // id 11, 12, 21, 22
    double beta = epsxy / epsx;
    double alpha = meany - beta * meanx;
    double eps = 0;
    double x2 = 0;
    for (int i = 0; i < n; ++i)
    {
        eps += (y[i] - alpha - beta * x[i]) * (y[i] - alpha - beta * x[i]);
        x2 += x[i] * x[i];
    }
    switch (oid)
    {
    case (11):
    {
        return sqrt(eps / epsx * x2 / (n - 2) / n);
        break;
    }
    case (12):
    {
        return alpha / sqrt(eps / epsx * x2 / (n - 2) / n);
        break;
    }
    case (21):
    {
        return sqrt(eps / epsx / (n - 2));
        break;
    }
    case (22):
    {
        return beta / sqrt(eps / epsx / (n - 2));
        break;
    }
    default:
    {
        throw std::invalid_argument("output_id must be [0/1/2/11/12/21/22]");
        return std::nan("1");
    }
    }
}
