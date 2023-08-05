from AnnotatedTree.Layer.MultiWordMultiItemLayer cimport MultiWordMultiItemLayer


cdef class MetaMorphemesMovedLayer(MultiWordMultiItemLayer):

    cpdef setLayerValue(self, str layerValue)
    cpdef int getLayerSize(self, object viewLayer)
    cpdef str getLayerInfoAt(self, object viewLayer, int index)
