cdef class NodeDrawableCollector:

    def __init__(self, rootNode: ParseNodeDrawable, condition: NodeDrawableCondition):
        self.__rootNode = rootNode
        self.__condition = condition

    cpdef collectNodes(self, ParseNodeDrawable parseNode, list collected):
        cdef int i
        if self.__condition is None or self.__condition.satisfies(parseNode):
            collected.append(parseNode)
        for i in range(parseNode.numberOfChildren()):
            self.collectNodes(parseNode.getChild(i), collected)

    cpdef list collect(self):
        cdef list result
        result = []
        self.collectNodes(self.__rootNode, result)
        return result
