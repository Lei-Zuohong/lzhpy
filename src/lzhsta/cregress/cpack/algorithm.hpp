#pragma once
#include "typedef.hpp"

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
