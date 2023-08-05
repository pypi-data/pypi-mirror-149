from AnnotatedTree.Processor.Condition.IsNullElement cimport IsNullElement


cdef class IsEnglishLeafNode(IsLeafNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        if parseNode.numberOfChildren() == 0:
            return not IsNullElement().satisfies(parseNode)
        return False
