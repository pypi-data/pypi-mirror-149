from MorphologicalAnalysis.MetamorphicParse cimport MetamorphicParse
from AnnotatedTree.Layer.MetaMorphemesMovedLayer cimport MetaMorphemesMovedLayer


cdef class MetaMorphemeLayer(MetaMorphemesMovedLayer):

    cpdef setLayerValueWithMetamorphicParse(self, MetamorphicParse layerValue)
    cpdef str getLayerInfoFrom(self, int index)
    cpdef MetamorphicParse metaMorphemeRemoveFromIndex(self, int index)
