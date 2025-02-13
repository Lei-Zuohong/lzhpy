# cython: boundcheck=False, wraparound=False, initializedcheck=False, cdivision=True, nonecheck=False
from libcpp.vector cimport vector
from cython.parallel cimport prange

cdef extern from "cpack/linear.hpp":
    double regression_linear_fast(vector[double] x, vector[double] y, int output_id) nogil

cdef extern from "cpack/multi.hpp":
    vector[double] regression_multi_fast(vector[vector[double]] x, vector[double] y, int output_id) nogil

cdef struct result_linear:
    int codex
    int codey
    double output

cdef struct result_multi:
    int code
    vector[double] output

def fit_cross(codes, x, y, output_id, jobN):
    cdef:
        int codeN = len(codes)
        int index
        vector[int] temp_index_xy = [0, 0]
        vector[vector[int]] index_xy
        result_linear result
        vector[result_linear] results

    for indexx in range(codeN):
        for indexy in range(codeN):
            if indexx != indexy:
                temp_index_xy = [indexx, indexy]
                index_xy.push_back(temp_index_xy)
                results.push_back(result)

    cdef:
        int indexN = len(index_xy)
        int num_threads = jobN
        vector[int] codes_c = codes
        vector[vector[double]] x_c = x
        vector[vector[double]] y_c = y
        int output_id_c = output_id

    for index in prange(indexN, nogil=True, schedule='static', num_threads=num_threads):
        fill_cross(codes_c[index_xy[index][0]],
                   codes_c[index_xy[index][1]],
                   x_c[index_xy[index][0]],
                   y_c[index_xy[index][1]],
                   output_id_c,
                   results[index])
    
    return results

def fit_across(codexs, codeys, x, y, output_id, jobN):
    cdef:
        int index
        vector[int] temp_index_xy = [0, 0]
        vector[vector[int]] index_xy
        result_linear result
        vector[result_linear] results

    for indexx in range(len(codexs)):
        for indexy in range(len(codeys)):
            temp_index_xy = [indexx, indexy]
            index_xy.push_back(temp_index_xy)
            results.push_back(result)

    cdef:
        int indexN = len(index_xy)
        int num_threads = jobN
        vector[int] codexs_c = codexs
        vector[int] codeys_c = codeys
        vector[vector[double]] x_c = x
        vector[vector[double]] y_c = y
        int output_id_c = output_id

    for index in prange(indexN, nogil=True, schedule='static', num_threads=num_threads):
        fill_cross(codexs_c[index_xy[index][0]],
                   codeys_c[index_xy[index][1]],
                   x_c[index_xy[index][0]],
                   y_c[index_xy[index][1]],
                   output_id_c,
                   results[index])
    
    return results

cdef int fill_cross(int codex, int codey, vector[double] x, vector[double] y, int output_id, result_linear &result) nogil:
    result.codex = codex
    result.codey = codey
    result.output = regression_linear_fast(x, y, output_id)
    return 1

def fit_path(codes, x, y, output_id, jobN):
    cdef:
        int codeN = len(codes)
        int index
        int num_threads = jobN
        vector[int] codes_c = codes
        vector[vector[vector[double]]] x_c = x
        vector[vector[double]] y_c = y
        result_multi result
        vector[result_multi] results
        int output_id_c = output_id

    for index in range(codeN):
        results.push_back(result)
    
    for index in prange(codeN, nogil=True, schedule='static', num_threads=num_threads):
        fill_path(codes_c[index],
                  x_c[index],
                  y_c[index],
                  index,
                  output_id_c,
                  results[index])
    
    return results

cdef int fill_path(int code, vector[vector[double]] x, vector[double] y, int index, int output_id, result_multi &result) nogil:
    result.code = code
    result.output = regression_multi_fast(x, y, output_id)
    return 1