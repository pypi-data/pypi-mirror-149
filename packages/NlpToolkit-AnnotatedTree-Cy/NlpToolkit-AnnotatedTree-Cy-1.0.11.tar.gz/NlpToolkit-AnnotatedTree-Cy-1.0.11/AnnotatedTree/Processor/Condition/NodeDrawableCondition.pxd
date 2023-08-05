from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable


cdef class NodeDrawableCondition:

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)
