from AnnotatedTree.Layer.WordLayer cimport WordLayer


cdef class SingleWordLayer(WordLayer):

    cpdef setLayerValue(self, str layerValue)
