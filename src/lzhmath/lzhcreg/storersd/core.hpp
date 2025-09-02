#pragma once
#include <cmath>
#include <string>
#include <vector>
#include <iostream>

using Vdouble = std::vector<double>;
using VVdouble = std::vector<Vdouble>;
using VVVdouble = std::vector<VVdouble>;

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
            matrix1[i][i] = 0.0000000000000001;
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

// datax (paraN * sampleN)
// datay (outputN)
Vdouble reg_storersd(const Vdouble datay, const VVdouble datax)
{
    int paraN = datax.size();
    int dataN = datax[0].size();
    // 1: build x, y
    VVdouble x;
    Vdouble y;
    x.assign(datax.begin(), datax.end());
    x.push_back(Vdouble(dataN, 1));
    y.assign(datay.begin(), datay.end());

    // 2: reverse x
    VVdouble xtwx(paraN + 1, Vdouble(paraN + 1, 0));
    for (int i = 0; i < paraN + 1; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            for (int k = 0; k < dataN; k++)
            {
                xtwx[i][j] += x[i][k] * x[j][k];
            }
        }
    }
    xtwx = matrix_inverse(xtwx);
    // 3: beta
    Vdouble beta(paraN + 1, 0);
    for (int i = 0; i < paraN + 1; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            for (int k = 0; k < dataN; k++)
            {
                beta[i] += xtwx[i][j] * x[j][k] * y[k];
            }
        }
    }
    // 4: yp
    Vdouble yp(dataN, 0);
    for (int i = 0; i < dataN; i++)
    {
        for (int j = 0; j < paraN + 1; j++)
        {
            yp[i] += beta[j] * x[j][i];
        }
    }
    // 5: r
    double meany = 0;
    double meanyp = 0;
    double ssty = 0;
    double ssry = 0;
    double r = 0;
    for (int i = 0; i < dataN; i++)
    {
        meany += y[i];
        meanyp += yp[i];
    }
    meany /= dataN;
    meanyp /= dataN;
    for (int i = 0; i < dataN; i++)
    {
        ssty += (y[i] - meany) * (y[i] - meany);
        ssry += (yp[i] - meanyp) * (yp[i] - meanyp);
    }
    if (ssty <= 0)
    {
        beta = Vdouble(paraN + 1, 0);
        r = 1;
    }
    else
    {
        r = sqrt(ssry / ssty);
    }
    // 6: output
    beta.push_back(r);
    return beta;
}