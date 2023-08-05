cdef class WordLayer:

    cdef str layerValue, layerName

    cpdef str getLayerValue(self)
    cpdef str getLayerName(self)
    cpdef str getLayerDescription(self)
