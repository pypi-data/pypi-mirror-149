cdef class ShallowParseLayer(MultiWordLayer):

    def __init__(self, layerValue: str):
        self.layerName = "shallowParse"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        cdef list splitParse
        self.items = []
        self.layerValue = layerValue
        if layerValue is not None:
            splitParse = layerValue.split(" ")
            self.items.extend(splitParse)
