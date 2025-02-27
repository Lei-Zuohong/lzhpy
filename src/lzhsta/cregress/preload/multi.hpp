#pragma once
#include <cmath>
#include <stdexcept>
#include "typedef.hpp"

// (VVdouble, Vdouble)
// return double
// (VVdouble, Vdouble, int)
// return Vdouble
// oid: 2   =>   out: beta
// oid: 21  =>   out: beta_e
// oid: 22  =>   out: beta_t

VVdouble matrix_inverse(VVdouble input_matrix)
{
    int size = input_matrix.size();
    VVdouble matrix1, matrix2;
    matrix1.assign(input_matrix.begin(), input_matrix.end());
    matrix2 = VVdouble(size, Vdouble(size, 0));
    for (int i = 0; i < size; i++)
    {
        matrix2[i][i] = 1;
    }
    double tempd;
    Vdouble tempv;
    for (int i = 0; i < size; i++)
    {
        if (matrix1[i][i] == 0)
        {
            for (int j = i + 1; j < size; j++)
            {
                if (matrix1[j][i] != 0)
                {
                    tempv = matrix1[i];
                    matrix1[i] = matrix1[j];
                    matrix1[j] = tempv;
                    tempv = matrix2[i];
                    matrix2[i] = matrix2[j];
                    matrix2[j] = tempv;
                    break;
                }
            }
        }
        if (matrix1[i][i] == 0)
        {
            matrix1[i][i] = 0.0000000001;
        }
        tempd = matrix1[i][i];
        for (int j = 0; j < size; j++)
        {
            matrix1[i][j] /= tempd;
            matrix2[i][j] /= tempd;
        }
        for (int j = 0; j < size; j++)
        {
            if (j != i)
            {
                tempd = matrix1[j][i];
                for (int k = 0; k < size; k++)
                {
                    matrix1[j][k] -= tempd * matrix1[i][k];
                    matrix2[j][k] -= tempd * matrix2[i][k];
                }
            }
        }
    }
    return matrix2;
}
double regression_multi_r(VVdouble x, Vdouble y)
{
    int paraN = x.size();
    int dataN = x[0].size();
    VVdouble x_;
    VVdouble xtwx(paraN + 1, Vdouble(paraN + 1, 0));
    Vdouble beta(paraN + 1, 0);
    Vdouble yp_(dataN, 0);
    x_.assign(x.begin(), x.end());
    x_.push_back(Vdouble(x[0].size(), 1));
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
    for (int i = 0; i < dataN; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            yp_[i] += beta[j] * x_[j][i];
        }
    }
    double meany = 0;
    double meanyp = 0;
    double ssty = 0;
    double ssry = 0;
    for (int i = 0; i < dataN; i++)
    {
        meany += y[i];
        meanyp += yp_[i];
    }
    meany /= dataN;
    meanyp /= dataN;
    for (int i = 0; i < dataN; i++)
    {
        ssty += (y[i] - meany) * (y[i] - meany);
        ssry += (yp_[i] - meanyp) * (yp_[i] - meanyp);
    }
    if (ssty <= 0)
    {
        return std::nan("1");
    }
    double output = sqrt(ssry / ssty);
    return output;
}
Vdouble regression_multi(VVdouble x, Vdouble y, int oid)
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
    if (oid == 2)
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
    if (oid == 0)
    {
        double meany = 0;
        double meanyp = 0;
        double ssty = 0;
        double ssry = 0;
        for (int i = 0; i < dataN; i++)
        {
            meany += y[i];
            meanyp += yp_[i];
        }
        meany /= dataN;
        meanyp /= dataN;
        for (int i = 0; i < dataN; i++)
        {
            ssty += (y[i] - meany) * (y[i] - meany);
            ssry += (yp_[i] - meanyp) * (yp_[i] - meanyp);
        }
        double output = sqrt(ssry / ssty);
        return {output};
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
    if (oid == 21)
    {
        return beta_e;
    }
    if (oid == 22)
    {
        for (int i = 0; i < paraN + 1; i++)
        {
            beta_e[i] = beta[i] / beta_e[i];
        }
        return beta_e;
    }
    throw std::invalid_argument("method must be [2/21/22]");
    return Vdouble(paraN + 1, std::nan("1"));
}
