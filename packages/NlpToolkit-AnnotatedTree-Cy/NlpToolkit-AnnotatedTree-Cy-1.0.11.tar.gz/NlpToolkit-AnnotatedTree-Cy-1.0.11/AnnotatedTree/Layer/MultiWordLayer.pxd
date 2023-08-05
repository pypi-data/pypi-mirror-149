from AnnotatedTree.Layer.WordLayer cimport WordLayer


cdef class MultiWordLayer(WordLayer):

    cdef list items

    cpdef object getItemAt(self, int index)
    cpdef int size(self)
    cpdef setLayerValue(self, str layerValue)
