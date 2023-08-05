from AnnotatedTree.LayerInfo cimport LayerInfo
from WordNet.WordNet cimport WordNet


cdef class IsPredicateVerbNode(IsVerbNode):

    def __init__(self, wordNet: WordNet):
        super().__init__(wordNet)

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef LayerInfo layerInfo
        layerInfo = parseNode.getLayerInfo()
        return super().satisfies(parseNode) and layerInfo is not None and layerInfo.getArgument() is not None \
               and layerInfo.getArgument().getArgumentType() == "PREDICATE"
