from AnnotatedTree.Processor.Condition.IsNoneNode cimport IsNoneNode
from AnnotatedTree.Processor.Condition.IsNullElement cimport IsNullElement
from AnnotatedSentence.ViewLayerType import ViewLayerType


cdef class IsTransferable(IsLeafNode):

    def __init__(self, secondLanguage: ViewLayerType):
        self.__secondLanguage = secondLanguage

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        if parseNode.numberOfChildren() == 0:
            if IsNoneNode(self.__secondLanguage).satisfies(parseNode):
                return False
            return not IsNullElement().satisfies(parseNode)
        return False
