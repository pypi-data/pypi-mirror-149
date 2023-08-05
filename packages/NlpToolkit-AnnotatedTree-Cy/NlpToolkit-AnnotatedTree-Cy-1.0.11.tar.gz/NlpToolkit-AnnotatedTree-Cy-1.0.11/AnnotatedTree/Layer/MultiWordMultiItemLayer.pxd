from AnnotatedTree.Layer.MultiWordLayer cimport MultiWordLayer


cdef class MultiWordMultiItemLayer(MultiWordLayer):

    cpdef int getLayerSize(self, object viewLayer)
    cpdef str getLayerInfoAt(self, object viewLayer, int index)
