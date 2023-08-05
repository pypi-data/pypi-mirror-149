from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.NodeDrawableCondition cimport NodeDrawableCondition


cdef class IsLeafNode(NodeDrawableCondition):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)
