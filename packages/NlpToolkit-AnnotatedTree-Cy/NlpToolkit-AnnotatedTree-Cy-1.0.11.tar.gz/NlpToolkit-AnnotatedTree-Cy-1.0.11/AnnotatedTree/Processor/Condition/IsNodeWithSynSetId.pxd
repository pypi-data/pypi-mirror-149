from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsLeafNode cimport IsLeafNode


cdef class IsNodeWithSynSetId(IsLeafNode):

    cdef str __id

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)
