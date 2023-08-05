from AnnotatedTree.Layer.MultiWordLayer cimport MultiWordLayer


cdef class ShallowParseLayer(MultiWordLayer):

    cpdef setLayerValue(self, str layerValue)
