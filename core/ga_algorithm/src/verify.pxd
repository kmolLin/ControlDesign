# -*- coding: utf-8 -*-
# cython: language_level=3

"""The callable class of the validation in algorithm."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from numpy cimport ndarray


cdef enum limit:
    maxGen, minFit, maxTime


cdef class Chromosome:
    cdef public int n
    cdef public double f
    cdef public ndarray v
    
    cdef double distance(self, Chromosome obj)
    cpdef void assign(self, Chromosome obj)


cdef class Verification:
    cdef ndarray get_upper(self)
    cdef ndarray get_lower(self)
    cdef int get_nParm(self)
    cdef double run(self, ndarray v)
    cpdef object get_result(self, ndarray v)
