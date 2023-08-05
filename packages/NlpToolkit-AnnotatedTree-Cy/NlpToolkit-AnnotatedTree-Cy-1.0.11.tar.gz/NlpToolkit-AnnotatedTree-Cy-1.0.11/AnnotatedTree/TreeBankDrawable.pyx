import os
import re

from Corpus.FileDescription cimport FileDescription

cdef class TreeBankDrawable(TreeBank):

    def __init__(self, folder: str = None, pattern: str = None):
        cdef ParseTreeDrawable parseTree
        self.parseTrees = []
        if str is not None:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    fileName = os.path.join(root, file)
                    if (pattern is None or pattern in fileName) and re.match("\\d+\\.", file):
                        parseTree = ParseTreeDrawable(fileName)
                        if parseTree.getRoot() is not None:
                            parseTree.setName(fileName)
                            parseTree.setFileDescription(FileDescription(root, file))
                            self.parseTrees.append(parseTree)

    cpdef list getParseTrees(self):
        return self.parseTrees

    cpdef ParseTreeDrawable get(self, int index):
        return self.parseTrees[index]

    cpdef clearLayer(self, object layerType):
        cdef ParseTreeDrawable tree
        for tree in self.parseTrees:
            if isinstance(tree, ParseTreeDrawable):
                tree.clearLayer(layerType)
                tree.saveWithFileName()

    cpdef removeTree(self, int index):
        self.parseTrees.pop(index)
