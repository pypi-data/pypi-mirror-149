from AnnotatedTree.Layer.MultiWordLayer cimport MultiWordLayer


cdef class TargetLanguageWordLayer(MultiWordLayer):

    cpdef setLayerValue(self, str layerValue)
    cpdef int getLayerSize(self, object viewLayer)
    cpdef str getLayerInfoAt(self, object viewLayer, int index)
