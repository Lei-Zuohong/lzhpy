#pragma once
#include "algorithm.hpp"
#include <cmath>
#include <stdexcept>

/*
output id:
    2: beta
    21: beta_e
    22: beta_t
*/

Vdouble regression_multi_fast(VVdouble x, Vdouble y, int output_id)
{
    int paraN = x.size();
    int dataN = x[0].size();
    VVdouble x_;
    x_.assign(x.begin(), x.end());
    x_.push_back(Vdouble(x[0].size(), 1));
    VVdouble xtwx(paraN + 1, Vdouble(paraN + 1, 0));
    for (int i = 0; i < paraN + 1; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            for (int k = 0; k < dataN; k++)
            {
                xtwx[i][j] += x_[i][k] * x_[j][k];
            }
        }
    }
    xtwx = matrix_inverse(xtwx);
    Vdouble beta(paraN + 1, 0);
    for (int i = 0; i < paraN + 1; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            for (int k = 0; k < dataN; k++)
            {
                beta[i] += xtwx[i][j] * x_[j][k] * y[k];
            }
        }
    }
    if (output_id == 2)
    {
        return beta;
    }
    Vdouble yp_(dataN, 0);
    for (int i = 0; i < dataN; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            yp_[i] += beta[j] * x_[j][i];
        }
    }
    for (int i = 0; i < dataN; i++)
    {
        yp_[i] = y[i] - yp_[i];
    }
    double mse_num = 0;
    double mse_den = 0;
    for (int i = 0; i < dataN; i++)
    {
        mse_num += yp_[i] * yp_[i];
        mse_den += 1;
    }
    VVdouble tempv = VVdouble(paraN + 1, Vdouble(paraN + 1, 0));
    for (int i = 0; i < paraN + 1; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            tempv[i][j] = xtwx[i][j] * mse_num / mse_den * dataN / (dataN - paraN - 1);
        }
    }
    Vdouble beta_e(paraN + 1, 0);
    for (int i = 0; i < paraN + 1; i++)
    {
        if (tempv[i][i] <= 0)
        {
            beta_e[i] = 0.0000001;
        }
        else
        {
            beta_e[i] = sqrt(tempv[i][i]);
        }
    }
    if (output_id == 21)
    {
        return beta_e;
    }
    if (output_id == 22)
    {
        for (int i = 0; i < paraN + 1; i++)
        {
            beta_e[i] = beta[i] / beta_e[i];
        }
        return beta_e;
    }
    throw std::invalid_argument("output id must be [2/21/22]");
    return Vdouble(0);
}