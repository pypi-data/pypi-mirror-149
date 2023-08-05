from ParseTree.TreeBank cimport TreeBank
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable


cdef class TreeBankDrawable(TreeBank):

    cpdef list getParseTrees(self)
    cpdef ParseTreeDrawable get(self, int index)
    cpdef clearLayer(self, object layerType)
    cpdef removeTree(self, int index)
