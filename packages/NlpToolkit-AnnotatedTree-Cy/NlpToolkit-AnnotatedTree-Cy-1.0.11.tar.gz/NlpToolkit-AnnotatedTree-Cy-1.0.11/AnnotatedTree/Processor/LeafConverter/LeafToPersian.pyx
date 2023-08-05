from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.Processor.LeafConverter.LeafToLanguageConverter cimport LeafToLanguageConverter


cdef class LeafToPersian(LeafToLanguageConverter):

    def __init__(self):
        self.viewLayerType = ViewLayerType.PERSIAN_WORD
