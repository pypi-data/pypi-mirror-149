from AnnotatedSentence.ViewLayerType import ViewLayerType
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse


cdef class MorphologicalAnalysisLayer(MultiWordMultiItemLayer):

    def __init__(self, layerValue: str):
        self.layerName = "morphologicalAnalysis"
        self.setLayerValue(layerValue)

    cpdef setLayerValue(self, str layerValue):
        cdef list splitWords
        cdef str word
        cdef MorphologicalParse parse
        self.items = []
        if isinstance(layerValue, str):
            self.layerValue = layerValue
            if layerValue is not None:
                splitWords = self.layerValue.split(" ")
                for word in splitWords:
                    self.items.append(MorphologicalParse(word))
        elif isinstance(layerValue, MorphologicalParse):
            parse = layerValue
            self.layerValue = parse.getTransitionList()
            self.items.append(parse)

    cpdef int getLayerSize(self, object viewLayer):
        cdef int size
        cdef MorphologicalParse parse
        size = 0
        if viewLayer == ViewLayerType.PART_OF_SPEECH:
            for parse in self.items:
                if isinstance(parse, MorphologicalParse):
                    size += parse.tagSize()
        elif viewLayer == ViewLayerType.INFLECTIONAL_GROUP:
            for parse in self.items:
                if isinstance(parse, MorphologicalParse):
                    size += parse.size()
        return size

    cpdef str getLayerInfoAt(self, object viewLayer, int index):
        cdef int size
        cdef MorphologicalParse parse
        size = 0
        if viewLayer == ViewLayerType.PART_OF_SPEECH:
            for parse in self.items:
                if isinstance(parse, MorphologicalParse) and index < size + parse.tagSize():
                    return parse.getTag(index - size)
                size += parse.tagSize()
            return None
        elif viewLayer == ViewLayerType.INFLECTIONAL_GROUP:
            for parse in self.items:
                if isinstance(parse, MorphologicalParse) and index < size + parse.size():
                    return parse.getInflectionalGroupString(index - size)
                size += parse.size()
            return None
        return None
