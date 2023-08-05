cdef class TurkishSemanticLayer(MultiWordLayer):

    def __init__(self, layerValue: str):
        self.layerName = "semantics"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        cdef list splitMeanings
        self.items = []
        self.layerValue = layerValue
        if layerValue is not None:
            splitMeanings = layerValue.split("\\$")
            self.items.extend(splitMeanings)
