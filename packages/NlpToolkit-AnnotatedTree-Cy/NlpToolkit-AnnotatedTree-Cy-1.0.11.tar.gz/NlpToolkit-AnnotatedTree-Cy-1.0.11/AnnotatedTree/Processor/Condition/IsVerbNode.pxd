from WordNet.WordNet cimport WordNet
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsLeafNode cimport IsLeafNode


cdef class IsVerbNode(IsLeafNode):

    cdef WordNet __wordNet

    cpdef bint satisfies(self, ParseNodeDrawable parseNode)