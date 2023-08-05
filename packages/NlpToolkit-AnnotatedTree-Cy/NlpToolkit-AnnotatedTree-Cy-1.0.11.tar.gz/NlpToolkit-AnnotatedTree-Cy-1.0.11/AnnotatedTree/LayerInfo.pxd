from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from MorphologicalAnalysis.MetamorphicParse cimport MetamorphicParse
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse
from PropBank.Argument cimport Argument


cdef class LayerInfo:

    cdef dict layers

    cpdef setLayerData(self, object viewLayer, str layerValue)
    cpdef setMorphologicalAnalysis(self, MorphologicalParse parse)
    cpdef setMetaMorphemes(self, MetamorphicParse parse)
    cpdef bint layerExists(self, object viewLayerType)
    cpdef object checkLayer(self, object viewLayer)
    cpdef int getNumberOfWords(self)
    cpdef str getMultiWordAt(self, object viewLayerType, int index, str layerName)
    cpdef str getTurkishWordAt(self, int index)
    cpdef int getNumberOfMeanings(self)
    cpdef str getSemanticAt(self, int index)
    cpdef str getShallowParseAt(self, int index)
    cpdef Argument getArgument(self)
    cpdef Argument getArgumentAt(self, int index)
    cpdef MorphologicalParse getMorphologicalParseAt(self, int index)
    cpdef MetamorphicParse getMetamorphicParseAt(self, int index)
    cpdef str getMetaMorphemeAtIndex(self, int index)
    cpdef str getMetaMorphemeFromIndex(self, int index)
    cpdef int getLayerSize(self, object viewLayer)
    cpdef str getLayerInfoAt(self, object viewLayer, int index)
    cpdef str getLayerDescription(self)
    cpdef str getLayerData(self, object viewLayer)
    cpdef str getRobustLayerData(self, object viewLayer)
    cpdef updateMetaMorphemesMoved(self)
    cpdef removeLayer(self, object layerType)
    cpdef metaMorphemeClear(self)
    cpdef englishClear(self)
    cpdef dependencyLayer(self)
    cpdef metaMorphemesMovedClear(self)
    cpdef semanticClear(self)
    cpdef englishSemanticClear(self)
    cpdef morphologicalAnalysisClear(self)
    cpdef MetamorphicParse metaMorphemeRemove(self, int index)
    cpdef divideIntoWords(self)
    cpdef AnnotatedWord toAnnotatedWord(self, int wordIndex)
