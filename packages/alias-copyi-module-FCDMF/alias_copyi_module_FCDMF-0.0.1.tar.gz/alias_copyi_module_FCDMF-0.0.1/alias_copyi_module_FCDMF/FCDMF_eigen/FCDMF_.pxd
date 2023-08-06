from libcpp.vector cimport vector

cdef extern from "FCDMF.cpp":
    pass

cdef extern from "FCDMF.h":
    cdef cppclass FCDMF:
        vector[int] y

        FCDMF() except+
        FCDMF(vector[vector[double]] &B, int c_true) except+
        void opt(int ITER, vector[int] &p, vector[int] &q, int a1, int a2)
