from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable


cdef class LeafToStringConverter:

    cpdef str leafConverter(self, ParseNodeDrawable leafNode)
