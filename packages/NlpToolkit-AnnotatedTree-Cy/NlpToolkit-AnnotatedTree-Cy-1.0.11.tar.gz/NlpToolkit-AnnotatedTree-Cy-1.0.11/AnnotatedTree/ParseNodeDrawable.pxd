from NamedEntityRecognition.Gazetteer cimport Gazetteer
from ParseTree.ParseNode cimport ParseNode
from ParseTree.Symbol cimport Symbol
from AnnotatedTree.LayerInfo cimport LayerInfo


cdef class ParseNodeDrawable(ParseNode):

    cdef LayerInfo layers
    cdef int depth

    cpdef LayerInfo getLayerInfo(self)
    cpdef Symbol getData(self)
    cpdef clearLayers(self)
    cpdef clearLayer(self, object layerType)
    cpdef clearData(self)
    cpdef setDataAndClearLayers(self, Symbol data)
    cpdef setData(self, Symbol data)
    cpdef str headWord(self, object viewLayerType)
    cpdef str getLayerData(self, viewLayer=*)
    cpdef getDepth(self)
    cpdef updateDepths(self, int depth)
    cpdef int maxDepth(self)
    cpdef str ancestorString(self)
    cpdef bint layerExists(self, object viewLayerType)
    cpdef bint isDummyNode(self)
    cpdef bint layerAll(self, viewLayerType)
    cpdef str toTurkishSentence(self)
    cpdef generateParseNode(self, ParseNode parseNode, bint surfaceForm)
    cpdef checkGazetteer(self, Gazetteer gazetteer, str word)
