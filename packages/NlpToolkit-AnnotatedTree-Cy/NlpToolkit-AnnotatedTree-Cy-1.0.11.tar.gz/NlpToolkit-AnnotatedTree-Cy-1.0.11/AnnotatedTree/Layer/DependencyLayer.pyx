cdef class DependencyLayer(SingleWordLayer):

    def __init__(self, layerValue: str):
        self.layerName = "dependency"
        self.setLayerValue(layerValue)
