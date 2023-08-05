from PropBank.Argument cimport Argument


cdef class EnglishPropbankLayer(SingleWordMultiItemLayer):

    def __init__(self, layerValue: str):
        self.layerName = "englishPropbank"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        cdef list splitWords
        cdef str word
        self.items = []
        self.layerValue = layerValue
        if layerValue is not None:
            splitWords = layerValue.split("#")
            for word in splitWords:
                self.items.append(Argument(word))
