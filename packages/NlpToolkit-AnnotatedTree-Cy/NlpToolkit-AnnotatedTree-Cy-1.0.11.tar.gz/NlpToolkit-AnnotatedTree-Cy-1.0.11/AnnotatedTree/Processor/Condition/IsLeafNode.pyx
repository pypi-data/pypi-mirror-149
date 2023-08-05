cdef class IsLeafNode(NodeDrawableCondition):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        return parseNode.numberOfChildren() == 0
