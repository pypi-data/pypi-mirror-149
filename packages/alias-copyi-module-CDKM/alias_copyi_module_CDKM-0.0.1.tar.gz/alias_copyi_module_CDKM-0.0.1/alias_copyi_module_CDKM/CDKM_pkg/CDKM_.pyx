cimport numpy as np
import numpy as np
np.import_array()

from .CDKM_ cimport CDKM

cdef class PyCDKM:
    cdef CDKM c_CDKM
    cdef int N
    cdef int c_true

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, int debug=0):
        self.c_CDKM = CDKM(X, c_true, debug)
        self.N = X.shape[0]
        self.c_true = c_true

    def opt(self, init_Y, int ITER=300):
        self.c_CDKM.opt(init_Y, ITER)

    @property
    def y_pre(self):
        return np.array(self.c_CDKM.Y)
    
    @property
    def n_iter_(self):
        return np.array(self.c_CDKM.n_iter_)
