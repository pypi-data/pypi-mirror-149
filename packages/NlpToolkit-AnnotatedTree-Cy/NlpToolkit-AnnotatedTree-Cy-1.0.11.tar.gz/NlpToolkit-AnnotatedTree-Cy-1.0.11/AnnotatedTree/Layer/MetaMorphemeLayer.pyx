from AnnotatedSentence.ViewLayerType import ViewLayerType


cdef class MetaMorphemeLayer(MetaMorphemesMovedLayer):

    def __init__(self, layerValue: str):
        super().__init__(layerValue)
        self.layerName = "metaMorphemes"

    cpdef setLayerValueWithMetamorphicParse(self, MetamorphicParse layerValue):
        cdef list splitWords
        cdef str word
        if isinstance(layerValue, MetamorphicParse):
            parse = layerValue
            self.layerValue = parse.__str__()
            self.items = []
            if layerValue is not None:
                splitWords = self.layerValue.split(" ")
                for word in splitWords:
                    self.items.append(MetamorphicParse(word))

    cpdef str getLayerInfoFrom(self, int index):
        cdef int size
        cdef MetamorphicParse parse
        cdef str result
        size = 0
        for parse in self.items:
            if isinstance(parse, MetamorphicParse) and index < size + parse.size():
                result = parse.getMetaMorpheme(index - size)
                index = index + 1
                while index < size + parse.size():
                    result = result + "+" + parse.getMetaMorpheme(index - size)
                    index = index + 1
                return result
            size += parse.size()
        return None

    cpdef MetamorphicParse metaMorphemeRemoveFromIndex(self, int index):
        cdef int size
        cdef MetamorphicParse parse
        if 0 <= index < self.getLayerSize(ViewLayerType.META_MORPHEME):
            size = 0
            for parse in self.items:
                if isinstance(parse, MetamorphicParse) and index < size + parse.size():
                    parse.removeMetaMorphemeFromIndex(index - size)
                    return parse
            size += parse.size()
        return None
