from libcpp.vector cimport vector

cdef extern from "CDKM.cpp":
    pass

cdef extern from "CDKM.h":
    cdef cppclass CDKM:
        int N
        int dim
        int c_true
        int debug
        vector[vector[double]] X2
        vector[vector[int]] Y
        vector[int] n_iter_

        CDKM() except +
        CDKM(vector[vector[double]] &X, int c_true, int debug) except +
        void opt(vector[vector[int]] &init_Y, int ITER)
