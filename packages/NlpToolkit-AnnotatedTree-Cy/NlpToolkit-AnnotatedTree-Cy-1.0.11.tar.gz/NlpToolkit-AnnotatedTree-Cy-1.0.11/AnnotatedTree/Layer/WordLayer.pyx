cdef class WordLayer:

    cpdef str getLayerValue(self):
        return self.layerValue

    cpdef str getLayerName(self):
        return self.layerName

    cpdef str getLayerDescription(self):
        return "{" + self.layerName + "=" + self.layerValue + "}"
