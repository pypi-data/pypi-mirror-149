cdef class SingleWordLayer(WordLayer):

    cpdef setLayerValue(self, str layerValue):
        self.layerValue = layerValue
