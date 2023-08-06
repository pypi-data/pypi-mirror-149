#cython: language_level=3

cdef class TabFormat:
    cdef bint header
    cdef bint first_line
    cdef bytes NAString
    cdef set   tags
    cdef bytes sep
    cdef bint NAIntTo0
    cdef bint metabaR
    cdef bint ngsfilter
