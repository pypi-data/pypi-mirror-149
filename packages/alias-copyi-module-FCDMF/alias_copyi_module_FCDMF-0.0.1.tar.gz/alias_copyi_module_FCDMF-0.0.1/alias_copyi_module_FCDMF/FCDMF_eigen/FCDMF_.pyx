cimport numpy as np
import numpy as np
np.import_array()

from libcpp cimport bool
import time
from .FCDMF_ cimport FCDMF


cdef class PyFCDMF():
    cdef FCDMF c_FCDMF
    cdef int num
    cdef int num_anchor
    cdef int c_true
    cdef double[:, :] B
    cdef int[:, :] Y
    cdef double[:] times
    cdef bool debug

    def __init__(self, np.ndarray[double, ndim=2] B, int c_true, bool debug):
        self.B = B
        self.debug = debug
        self.c_FCDMF = FCDMF(B, c_true)
        self.num = B.shape[0]
        self.num_anchor = B.shape[1]
        self.c_true = c_true

    def opt(self, init_P, init_Q, int ITER):
        rep = init_P.shape[0]
        Y = np.zeros((rep, self.num), dtype=np.int32)
        a1 = int(np.maximum(self.num/10/self.c_true, 1))
        a2 = int(np.maximum(self.num_anchor/10/self.c_true, 1))

        times = np.zeros(rep)

        for rep_i in range(rep):

            if self.debug:
                print(f"rep_i = {rep_i}, begin")

            t_start = time.time()

            p = init_P[rep_i]
            q = init_Q[rep_i]
            self.c_FCDMF.opt(ITER, p, q, a1, a2)
            Y[rep_i] = np.array(self.c_FCDMF.y)

            t_end = time.time()

            times[rep_i] = t_end - t_start
            if self.debug:
                print(f"rep_i = {rep_i}, end, time = {times[rep_i]}")

        self.Y = Y
        self.times = times

    @property
    def y_pre(self):
        return np.array(self.Y)

    @property
    def time_arr(self):
        return np.array(self.times)

    @property
    def ref(self):
        titile = "Fast Clustering with Co-Clustering via Discrete Non-negative matrix factorization for image identification, ICASSP, 2020"

