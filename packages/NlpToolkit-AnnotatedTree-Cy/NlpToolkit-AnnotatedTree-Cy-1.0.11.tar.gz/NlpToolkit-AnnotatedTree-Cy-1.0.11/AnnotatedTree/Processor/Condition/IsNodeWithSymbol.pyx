from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.NodeDrawableCondition cimport NodeDrawableCondition


cdef class IsNodeWithSymbol(NodeDrawableCondition):

    cdef str __symbol

    def __init__(self, symbol: str):
        self.__symbol = symbol

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        if parseNode.numberOfChildren() > 0:
            return parseNode.getData().__str__() == self.__symbol
        else:
            return False
