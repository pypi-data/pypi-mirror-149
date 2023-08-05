from AnnotatedTree.LayerInfo cimport LayerInfo


cdef class IsNodeWithSynSetId(IsLeafNode):

    def __init__(self, id: str):
        self.__id = id

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef LayerInfo layerInfo
        cdef int i
        cdef str synSetId
        if parseNode.numberOfChildren() == 0:
            layerInfo = parseNode.getLayerInfo()
            for i in range(layerInfo.getNumberOfMeanings()):
                synSetId = layerInfo.getSemanticAt(i)
                if synSetId == self.__id:
                    return True
        return False
