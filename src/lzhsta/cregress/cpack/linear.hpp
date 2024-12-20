#pragma once
#include "algorithm.hpp"
#include <cmath>
#include <stdexcept>

/*
output id:
    0: r
    1: alpha
    2: beta
    11: alpha_e
    12: alpha_t
    21: beta_e
    22: beta_t
*/

double regression_linear_fast(Vdouble x, Vdouble y, int output_id)

{
    // mean
    double xmean = 0;
    double ymean = 0;
    for (int i = 0; i < int(y.size()); i++)
    {
        xmean += x[i];
        ymean += y[i];
    }
    xmean /= x.size();
    ymean /= y.size();
    // epsilon x, y, xy
    double epsilonx = 0;
    double epsilony = 0;
    double epsilonxy = 0;
    for (int i = 0; i < int(y.size()); i++)
    {
        epsilonx += (x[i] - xmean) * (x[i] - xmean);
        epsilony += (y[i] - ymean) * (y[i] - ymean);
        epsilonxy += (x[i] - xmean) * (y[i] - ymean);
    }
    double beta = epsilonxy / epsilonx;
    if (output_id == 2)
    {
        return beta;
    }
    double alpha = ymean - beta * xmean;
    if (output_id == 1)
    {
        return alpha;
    }
    double r = epsilonxy / sqrt(epsilonx * epsilony);
    if (output_id == 0)
    {
        return r;
    }
    double epsilon = 0;
    double x2 = 0;
    for (int i = 0; i < int(y.size()); i++)
    {
        epsilon += (y[i] - alpha - beta * x[i]) * (y[i] - alpha - beta * x[i]);
        x2 += x[i] * x[i];
    }
    double beta_e = sqrt(epsilon / epsilonx / (y.size() - 2));
    if (output_id == 21)
    {
        return beta_e;
    }
    if (output_id == 22)
    {
        return beta / beta_e;
    }
    double alpha_e = beta_e * sqrt(x2 / y.size());
    if (output_id == 11)
    {
        return alpha_e;
    }
    if (output_id == 12)
    {
        return alpha / alpha_e;
    }
    throw std::invalid_argument("output id must be [0/1/2/11/12/21/22]");
    return 0;
}