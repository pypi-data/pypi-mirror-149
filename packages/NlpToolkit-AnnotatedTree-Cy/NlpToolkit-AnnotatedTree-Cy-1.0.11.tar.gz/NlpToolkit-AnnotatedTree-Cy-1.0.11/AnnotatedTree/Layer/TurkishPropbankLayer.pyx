cdef class TurkishPropbankLayer(SingleWordLayer):

    def __init__(self, layerValue: str):
        self.layerName = "propbank"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        self.layerValue = layerValue
        self.__propbank = Argument(layerValue)

    cpdef Argument getArgument(self):
        return self.__propbank

    cpdef str getLayerValue(self):
        return self.__propbank.getArgumentType() + "$" + self.__propbank.getId()
