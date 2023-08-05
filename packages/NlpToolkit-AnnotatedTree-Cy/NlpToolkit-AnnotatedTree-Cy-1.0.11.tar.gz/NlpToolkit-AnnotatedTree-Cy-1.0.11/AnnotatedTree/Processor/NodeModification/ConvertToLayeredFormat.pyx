from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.NodeModification.NodeModifier cimport NodeModifier


cdef class ConvertToLayeredFormat(NodeModifier):

    cpdef modifier(self, ParseNodeDrawable parseNode):
        cdef name
        if parseNode.isLeaf():
            name = parseNode.getData().getName()
            parseNode.clearLayers()
            parseNode.getLayerInfo().setLayerData(ViewLayerType.ENGLISH_WORD, name)
            parseNode.clearData()
