from AnnotatedSentence.ViewLayerType import ViewLayerType


cdef class ParseNodeDrawable(ParseNode):

    def __init__(self, parent: ParseNodeDrawable, line: str, isLeaf: bool, depth: int):
        cdef int parenthesisCount
        cdef str childLine
        cdef int i
        self.children = []
        self.parent = parent
        self.layers = None
        self.data = None
        self.depth = depth
        parenthesisCount = 0
        childLine = ""
        if isLeaf:
            if "{" not in line:
                self.data = Symbol(line)
            else:
                self.layers = LayerInfo(line)
        else:
            self.data = Symbol(line[1: line.index(" ")])
            if line.index(")") == line.rindex(")"):
                self.children.append(ParseNodeDrawable(self, line[line.index(" ") + 1: line.index(")")],
                                                       True, depth + 1))
            else:
                for i in range(line.index(" ") + 1, len(line)):
                    if line[i] != " " or parenthesisCount > 0:
                        childLine = childLine + line[i]
                    if line[i] == "(":
                        parenthesisCount = parenthesisCount + 1
                    elif line[i] == ")":
                        parenthesisCount = parenthesisCount - 1
                    if parenthesisCount == 0 and len(childLine) != 0:
                        self.children.append(ParseNodeDrawable(self, childLine.strip(), False, depth + 1))
                        childLine = ""

    cpdef LayerInfo getLayerInfo(self):
        return self.layers

    cpdef Symbol getData(self):
        if self.layers is None:
            return self.data
        else:
            return Symbol(self.getLayerData(ViewLayerType.ENGLISH_WORD))

    cpdef clearLayers(self):
        self.layers = LayerInfo()

    cpdef clearLayer(self, object layerType):
        if len(self.children) == 0 and self.layerExists(layerType):
            self.layers.removeLayer(layerType)
        for child in self.children:
            if isinstance(child, ParseNodeDrawable):
                child.clearLayer(layerType)

    cpdef clearData(self):
        self.data = None

    cpdef setDataAndClearLayers(self, Symbol data):
        super().setData(data)
        self.layers = None

    cpdef setData(self, Symbol data):
        if self.layers is None:
            super().setData(data)
        else:
            self.layers.setLayerData(ViewLayerType.ENGLISH_WORD, self.data.getName())

    cpdef str headWord(self, object viewLayerType):
        if len(self.children) > 0:
            return self.headChild().headWord(viewLayerType)
        else:
            return self.getLayerData(viewLayerType)

    cpdef str getLayerData(self, viewLayer=None):
        if viewLayer is None:
            if self.data is not None:
                return self.data.getName()
            return self.layers.getLayerDescription()
        else:
            if viewLayer == ViewLayerType.WORD or self.layers is None:
                return self.data.getName()
            else:
                return self.layers.getLayerData(viewLayer)

    cpdef getDepth(self):
        return self.depth

    cpdef updateDepths(self, int depth):
        cdef ParseNodeDrawable child
        self.depth = depth
        for child in self.children:
            if isinstance(child, ParseNodeDrawable):
                child.updateDepths(depth + 1)

    cpdef int maxDepth(self):
        cdef int depth
        cdef ParseNodeDrawable child
        depth = self.depth
        for child in self.children:
            if isinstance(child, ParseNodeDrawable):
                if child.maxDepth() > depth:
                    depth = child.maxDepth()
        return depth

    cpdef str ancestorString(self):
        if self.parent is None:
            return self.data.getName()
        else:
            if self.layers is None:
                return self.parent.ancestorString() + self.data.getName()
            else:
                return self.parent.ancestorString() + self.layers.getLayerData(ViewLayerType.ENGLISH_WORD)

    cpdef bint layerExists(self, object viewLayerType):
        cdef ParseNodeDrawable child
        if len(self.children) == 0:
            if self.getLayerData() is not None:
                return True
        else:
            for child in self.children:
                if isinstance(child, ParseNodeDrawable):
                    return True
        return False

    cpdef bint isDummyNode(self):
        cdef str data, parentData, targetData
        data = self.getLayerData(ViewLayerType.ENGLISH_WORD)
        if isinstance(self.parent, ParseNodeDrawable):
            parentData = self.parent.getLayerData(ViewLayerType.ENGLISH_WORD)
        else:
            parentData = None
        targetData = self.getLayerData(ViewLayerType.TURKISH_WORD)
        if data is not None and parentData is not None:
            if targetData is not None and "*" in targetData:
                return True
            return "*" in data or (data == "0" and parentData == "-NONE-")
        else:
            return False

    cpdef bint layerAll(self, viewLayerType):
        cdef ParseNodeDrawable child
        if len(self.children) == 0:
            if self.getLayerData(viewLayerType) is None and not self.isDummyNode():
                return False
        else:
            for child in self.children:
                if isinstance(child, ParseNodeDrawable):
                    if not child.layerAll(viewLayerType):
                        return False
        return True

    cpdef str toTurkishSentence(self):
        cdef ParseNodeDrawable child
        cdef str st
        if len(self.children) == 0:
            if self.getLayerData(ViewLayerType.TURKISH_WORD) is not None and not self.isDummyNode():
                return " " + self.getLayerData(ViewLayerType.TURKISH_WORD).replace("-LRB-", "(").\
                    replace("-RRB-", ")").replace("-LSB-", "[").replace("-RSB-", "]").replace("-LCB-", "{").\
                    replace("-RCB-", "}").replace("-lrb-", "(").replace("-rrb-", ")").replace("-lsb-", "[").\
                    replace("-rsb-", "]").replace("-lcb", "{").replace("-rcb-", "}")
            else:
                return " "
        else:
            st = ""
            for child in self.children:
                if isinstance(child, ParseNodeDrawable):
                    st += child.toSentence()
            return st

    cpdef checkGazetteer(self, Gazetteer gazetteer, str word):
        if gazetteer.contains(word) and self.getParent().getData().getName() == "NNP":
            self.getLayerInfo().setLayerData(ViewLayerType.NER, gazetteer.getName())
        if "'" in word and gazetteer.contains(word[:word.index("'")]) and self.getParent().getData().getName() == "NNP":
            self.getLayerInfo().setLayerData(ViewLayerType.NER, gazetteer.getName())

    cpdef generateParseNode(self, ParseNode parseNode, bint surfaceForm):
        if len(self.children) == 0:
            if surfaceForm:
                parseNode.setData(Symbol(self.getLayerData(ViewLayerType.TURKISH_WORD)))
            else:
                parseNode.setData(Symbol(self.getLayerInfo().getMorphologicalParseAt(0).getWord().getName()))
        else:
            parseNode.setData(self.data)
            for child in self.children:
                newChild = ParseNode("")
                parseNode.addChild(newChild)
                child.generateParseNode(newChild, surfaceForm)

    def __str__(self) -> str:
        cdef ParseNodeDrawable child
        if len(self.children) < 2:
            if len(self.children) < 1:
                return self.getLayerData()
            else:
                return "(" + self.data.getName() + " " + self.children[0].__str__() + ")"
        else:
            st = "(" + self.data.getName()
            for child in self.children:
                st = st + " " + child.__str__()
            return st + ") "
