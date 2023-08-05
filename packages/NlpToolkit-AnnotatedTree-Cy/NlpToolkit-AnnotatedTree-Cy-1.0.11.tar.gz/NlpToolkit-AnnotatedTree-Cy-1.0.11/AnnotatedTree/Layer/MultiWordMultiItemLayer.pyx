cdef class MultiWordMultiItemLayer(MultiWordLayer):

    cpdef int getLayerSize(self, object viewLayer):
        pass

    cpdef str getLayerInfoAt(self, object viewLayer, int index):
        pass
