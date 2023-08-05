from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsNodeWithSynSetId cimport IsNodeWithSynSetId
from AnnotatedTree.LayerInfo cimport LayerInfo


cdef class IsNodeWithPredicate(IsNodeWithSynSetId):

    def __init__(self, _id: str):
        super().__init__(_id)

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef LayerInfo layerInfo
        layerInfo = parseNode.getLayerInfo()
        return super().satisfies(parseNode) and layerInfo is not None and \
               layerInfo.getLayerData(ViewLayerType.PROPBANK) is not None and \
               layerInfo.getLayerData(ViewLayerType.PROPBANK) == "PREDICATE"
