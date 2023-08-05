from AnnotatedSentence.ViewLayerType import ViewLayerType
from Dictionary.Word import Word
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsLeafNode cimport IsLeafNode


cdef class IsPunctuationNode(IsLeafNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef str data
        if parseNode.numberOfChildren() == 0:
            data = parseNode.getLayerData(ViewLayerType.ENGLISH_WORD)
            return Word.isPunctuationSymbol(data) and data != "$"
        return False
