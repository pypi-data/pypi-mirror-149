from AnnotatedTree.Layer.MultiWordLayer cimport MultiWordLayer


cdef class TurkishSemanticLayer(MultiWordLayer):

    cpdef setLayerValue(self, str layerValue)
