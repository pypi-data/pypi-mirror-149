from PropBank.Argument cimport Argument
from AnnotatedTree.Layer.SingleWordLayer cimport SingleWordLayer


cdef class TurkishPropbankLayer(SingleWordLayer):

    cdef Argument __propbank

    cpdef setLayerValue(self, str layerValue)
    cpdef Argument getArgument(self)
    cpdef str getLayerValue(self)
