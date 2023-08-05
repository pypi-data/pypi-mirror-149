from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsVerbNode cimport IsVerbNode


cdef class IsPredicateVerbNode(IsVerbNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)
