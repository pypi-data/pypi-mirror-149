from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.LeafConverter.LeafToStringConverter cimport LeafToStringConverter


cdef class TreeToStringConverter:

    cdef LeafToStringConverter __converter
    cdef ParseTreeDrawable __parseTree

    def __init__(self, parseTree: ParseTreeDrawable, converter: LeafToStringConverter):
        self.__converter = converter
        self.__parseTree = parseTree

    cpdef convertToString(self, ParseNodeDrawable parseNode):
        cdef str st
        cdef int i
        if parseNode.isLeaf():
            return self.__converter.leafConverter(parseNode)
        else:
            st = ""
            for i in range(parseNode.numberOfChildren()):
                st += self.convertToString(parseNode.getChild(i))
            return st

    cpdef str convert(self):
        return self.convertToString(self.__parseTree.getRoot())
