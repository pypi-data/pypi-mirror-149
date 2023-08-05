from ParseTree.ParseTree cimport ParseTree
from Corpus.FileDescription cimport FileDescription
from ParseTree.ParseNode cimport ParseNode
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from WordNet.WordNet cimport WordNet


cdef class ParseTreeDrawable(ParseTree):

    cdef str __name
    cdef FileDescription __fileDescription

    cpdef setFileDescription(self, FileDescription fileDescription)
    cpdef FileDescription getFileDescription(self)
    cpdef reload(self)
    cpdef readFromFile(self, str fileName)
    cpdef setName(self, str name)
    cpdef str getName(self)
    cpdef nextTree(self, int count)
    cpdef previousTree(self, int count)
    cpdef saveWithFileName(self)
    cpdef saveWithPath(self, str newPath)
    cpdef int maxDepth(self)
    cpdef moveLeft(self, ParseNode node)
    cpdef moveRight(self, ParseNode node)
    cpdef bint layerExists(self, object viewLayerType)
    cpdef bint layerAll(self, object viewLayerType)
    cpdef clearLayer(self, object viewLayerType)
    cpdef AnnotatedSentence generateAnnotatedSentence(self, str language=*)
    cpdef ParseTree generateParseTree(self, bint surfaceForm)
    cpdef list extractNodesWithVerbs(self, WordNet wordNet)
    cpdef list extractNodesWithPredicateVerbs(self, WordNet wordNet)
