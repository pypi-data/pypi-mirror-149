from AnnotatedTree.Layer.MultiWordLayer cimport MultiWordLayer


cdef class TargetLanguageWordLayer(MultiWordLayer):

    def __init__(self, layerValue: str):
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        cdef list splitWords
        self.items = []
        self.layerValue = layerValue
        if layerValue is not None:
            splitWords = layerValue.split(" ")
            self.items.extend(splitWords)

    cpdef int getLayerSize(self, object viewLayer):
        return 0

    cpdef str getLayerInfoAt(self, object viewLayer, int index):
        return None
