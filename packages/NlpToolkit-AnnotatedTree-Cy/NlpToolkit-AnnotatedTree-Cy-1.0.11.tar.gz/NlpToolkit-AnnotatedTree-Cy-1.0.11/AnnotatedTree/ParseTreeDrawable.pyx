from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from AnnotatedTree.Processor.Condition.IsPredicateVerbNode cimport IsPredicateVerbNode
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode cimport IsTurkishLeafNode
from AnnotatedTree.Processor.Condition.IsEnglishLeafNode cimport IsEnglishLeafNode
from AnnotatedTree.Processor.Condition.IsVerbNode cimport IsVerbNode
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector
from AnnotatedTree.LayerInfo cimport LayerInfo


cdef class ParseTreeDrawable(ParseTree):

    def __init__(self, fileDescription, path: str=None):
        if path is None:
            if isinstance(fileDescription, FileDescription):
                self.__fileDescription = fileDescription
                self.readFromFile(self.__fileDescription.getFileName(fileDescription.getPath()))
            elif isinstance(fileDescription, str):
                self.readFromFile(fileDescription)
        else:
            self.__fileDescription = FileDescription(path, fileDescription.getExtension(), fileDescription.getIndex())
            self.readFromFile(self.__fileDescription.getFileName(fileDescription.getPath()))

    cpdef setFileDescription(self, FileDescription fileDescription):
        self.__fileDescription = fileDescription

    cpdef FileDescription getFileDescription(self):
        return self.__fileDescription

    cpdef reload(self):
        self.readFromFile(self.__fileDescription.getFileName(self.__fileDescription.getPath()))

    cpdef readFromFile(self, str fileName):
        cdef str line
        inputFile = open(fileName, encoding="utf8")
        line = inputFile.readline().strip()
        if "(" in line and ")" in line:
            line = line[line.index("(") + 1:line.rindex(")")].strip()
            self.root = ParseNodeDrawable(None, line, False, 0)
        else:
            self.root = None
        inputFile.close()

    cpdef setName(self, str name):
        self.__name = name

    cpdef str getName(self):
        return self.__name

    cpdef nextTree(self, int count):
        if self.__fileDescription.nextFileExists(count):
            self.__fileDescription.addToIndex(count)
            self.reload()

    cpdef previousTree(self, int count):
        if self.__fileDescription.previousFileExists(count):
            self.__fileDescription.addToIndex(-count)
            self.reload()

    cpdef saveWithFileName(self):
        outputFile = open(self.__fileDescription.getFileName(), mode='w', encoding="utf8")
        outputFile.write("( " + self.__str__() + " )\n")
        outputFile.close()

    cpdef saveWithPath(self, str newPath):
        outputFile = open(self.__fileDescription.getFileName(newPath), mode='w', encoding="utf8")
        outputFile.write("( " + self.__str__() + " )\n")
        outputFile.close()

    cpdef int maxDepth(self):
        if isinstance(self.root, ParseNodeDrawable):
            return self.root.maxDepth()

    cpdef moveLeft(self, ParseNode node):
        if self.root != node:
            self.root.moveLeft(node)

    cpdef moveRight(self, ParseNode node):
        if self.root != node:
            self.root.moveRight(node)

    cpdef bint layerExists(self, object viewLayerType):
        if self.root is not None and isinstance(self.root, ParseNodeDrawable):
            return self.root.layerExists(viewLayerType)
        else:
            return False

    cpdef bint layerAll(self, object viewLayerType):
        if self.root is not None and isinstance(self.root, ParseNodeDrawable):
            return self.root.layerAll(viewLayerType)
        else:
            return False

    cpdef clearLayer(self, object viewLayerType):
        if self.root is not None and isinstance(self.root, ParseNodeDrawable):
            self.root.clearLayer(viewLayerType)

    cpdef AnnotatedSentence generateAnnotatedSentence(self, str language=None):
        cdef AnnotatedSentence sentence
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef list leafList
        cdef int i
        cdef ParseNodeDrawable parseNode
        cdef LayerInfo layers
        sentence = AnnotatedSentence()
        if language is None:
            nodeDrawableCollector = NodeDrawableCollector(self.root, IsTurkishLeafNode())
            leafList = nodeDrawableCollector.collect()
            for parseNode in leafList:
                if isinstance(parseNode, ParseNodeDrawable):
                    layers = parseNode.getLayerInfo()
                    for i in range(layers.getNumberOfWords()):
                        sentence.addWord(layers.toAnnotatedWord(i))
        else:
            nodeDrawableCollector = NodeDrawableCollector(self.root, IsEnglishLeafNode())
        leafList = nodeDrawableCollector.collect()
        for parseNode in leafList:
            if isinstance(parseNode, ParseNodeDrawable):
                newWord = AnnotatedWord("{" + language + "=" + parseNode.getData().getName() + "}{posTag="
                                        + parseNode.getParent().getData().getName() + "}")
                sentence.addWord(newWord)
        return sentence

    cpdef ParseTree generateParseTree(self, bint surfaceForm):
        result = ParseTree(ParseNode(self.root.getData()))
        self.root.generateParseNode(result.getRoot(), surfaceForm)
        return result

    cpdef list extractNodesWithVerbs(self, WordNet wordNet):
        cdef NodeDrawableCollector nodeDrawableCollector
        nodeDrawableCollector = NodeDrawableCollector(self.root, IsVerbNode(wordNet))
        return nodeDrawableCollector.collect()

    cpdef list extractNodesWithPredicateVerbs(self, WordNet wordNet):
        cdef NodeDrawableCollector nodeDrawableCollector
        nodeDrawableCollector = NodeDrawableCollector(self.root, IsPredicateVerbNode(wordNet))
        return nodeDrawableCollector.collect()
