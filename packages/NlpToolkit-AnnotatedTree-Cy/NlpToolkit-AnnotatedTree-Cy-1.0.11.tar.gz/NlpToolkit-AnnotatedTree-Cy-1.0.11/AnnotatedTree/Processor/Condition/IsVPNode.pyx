from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.NodeDrawableCondition cimport NodeDrawableCondition


cdef class IsVPNode(NodeDrawableCondition):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        return parseNode.numberOfChildren() > 0 and parseNode.getData().isVP()
