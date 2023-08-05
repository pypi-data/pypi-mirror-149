from AnnotatedTree.Layer.SingleWordLayer cimport SingleWordLayer


cdef class SingleWordMultiItemLayer(SingleWordLayer):

    cdef list items

    cpdef object getItemAt(self, int index)
    cpdef getLayerSize(self, object viewLayer)
