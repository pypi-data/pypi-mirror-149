from AnnotatedTree.Layer.SingleWordMultiItemLayer cimport SingleWordMultiItemLayer


cdef class EnglishPropbankLayer(SingleWordMultiItemLayer):

    cpdef setLayerValue(self, str layerValue)
