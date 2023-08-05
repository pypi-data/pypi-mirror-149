from NamedEntityRecognition.NamedEntityType import NamedEntityType


cdef class NERLayer(SingleWordLayer):

    def __init__(self, layerValue: str):
        self.layerName = "namedEntity"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        self.layerValue = layerValue
        self.__namedEntity = NamedEntityType.getNamedEntityType(layerValue)

    cpdef str getLayerValue(self):
        return NamedEntityType.getNamedEntityString(self.__namedEntity)
