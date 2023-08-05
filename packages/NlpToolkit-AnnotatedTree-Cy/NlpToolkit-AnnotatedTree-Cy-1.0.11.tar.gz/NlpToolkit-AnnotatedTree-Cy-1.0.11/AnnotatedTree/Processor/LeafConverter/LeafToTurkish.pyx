from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.Processor.LeafConverter.LeafToLanguageConverter cimport LeafToLanguageConverter


cdef class LeafToTurkish(LeafToLanguageConverter):

    def __init__(self):
        self.viewLayerType = ViewLayerType.TURKISH_WORD
