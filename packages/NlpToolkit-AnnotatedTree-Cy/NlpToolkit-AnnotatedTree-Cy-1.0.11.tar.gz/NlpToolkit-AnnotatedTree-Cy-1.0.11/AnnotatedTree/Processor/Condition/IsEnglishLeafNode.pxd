from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsLeafNode cimport IsLeafNode


cdef class IsEnglishLeafNode(IsLeafNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)
