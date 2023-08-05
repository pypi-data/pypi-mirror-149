from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.NodeModification.NodeModifier cimport NodeModifier


cdef class TreeModifier:

    cdef ParseTreeDrawable __parseTree
    cdef NodeModifier __nodeModifier

    cpdef nodeModify(self, ParseNodeDrawable parseNode):
        cdef int i
        self.__nodeModifier.modifier(parseNode)
        for i in range(parseNode.numberOfChildren()):
            self.nodeModify(parseNode.getChild(i))

    cpdef modify(self):
        self.nodeModify(self.__parseTree.getRoot())

    def __init__(self, parseTree: ParseTreeDrawable, nodeModifier: NodeModifier):
        self.__parseTree = parseTree
        self.__nodeModifier = nodeModifier
