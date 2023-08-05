from AnnotatedTree.LayerInfo cimport LayerInfo
from AnnotatedSentence.ViewLayerType import ViewLayerType
from Dictionary.Pos import Pos


cdef class IsVerbNode(IsLeafNode):

    def __init__(self, wordNet: WordNet):
        self.__wordNet = wordNet

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef LayerInfo layerInfo
        cdef int i
        cdef str synSetId
        layerInfo = parseNode.getLayerInfo()
        if parseNode.numberOfChildren() == 0 and layerInfo is not None and \
            layerInfo.getLayerData(ViewLayerType.SEMANTICS) is not None:
            for i in range(layerInfo.getNumberOfMeanings()):
                synSetId = layerInfo.getSemanticAt(i)
                if self.__wordNet.getSynSetWithId(synSetId) is not None and \
                        self.__wordNet.getSynSetWithId(synSetId).getPos() == Pos.VERB:
                    return True
        return False
