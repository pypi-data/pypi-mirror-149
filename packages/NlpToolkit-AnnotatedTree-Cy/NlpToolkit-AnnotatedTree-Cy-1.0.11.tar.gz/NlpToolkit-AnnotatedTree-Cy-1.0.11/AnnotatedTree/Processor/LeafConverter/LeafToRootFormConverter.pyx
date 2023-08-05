from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.LeafConverter.LeafToStringConverter cimport LeafToStringConverter
from AnnotatedTree.LayerInfo cimport LayerInfo


cdef class LeafToRootFormConverter(LeafToStringConverter):

    cpdef str leafConverter(self, ParseNodeDrawable parseNodeDrawable):
        cdef str rootWords, root
        cdef int i
        cdef LayerInfo layerInfo
        layerInfo = parseNodeDrawable.getLayerInfo()
        rootWords = " "
        for i in range(layerInfo.getNumberOfWords()):
            root = layerInfo.getMorphologicalParseAt(i).getWord().getName()
            if root is not None and len(root) != 0:
                rootWords += " " + root
        return rootWords
