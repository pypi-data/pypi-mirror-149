from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable


cdef class NodeModifier:

    cpdef modifier(self, ParseNodeDrawable parseNode)
