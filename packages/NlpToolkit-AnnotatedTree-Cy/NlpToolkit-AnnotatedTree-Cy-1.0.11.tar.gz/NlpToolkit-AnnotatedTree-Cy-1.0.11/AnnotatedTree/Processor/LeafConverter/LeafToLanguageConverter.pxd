from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.LeafConverter.LeafToStringConverter cimport LeafToStringConverter


cdef class LeafToLanguageConverter(LeafToStringConverter):

    cdef object viewLayerType

    cpdef str leafConverter(self, ParseNodeDrawable leafNode)
