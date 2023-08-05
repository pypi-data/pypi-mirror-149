from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.TreeBankDrawable cimport TreeBankDrawable


cdef class ParallelTreeBankDrawable:

    cdef TreeBankDrawable __fromTreeBank
    cdef TreeBankDrawable __toTreeBank

    def __init__(self, folder1: str, folder2: str, pattern: str = None):
        self.__fromTreeBank = TreeBankDrawable(folder1, pattern)
        self.__toTreeBank = TreeBankDrawable(folder2, pattern)
        self.removeDifferentTrees()

    cpdef removeDifferentTrees(self):
        cdef int i, j
        i = 0
        j = 0
        while i < self.__fromTreeBank.size() and j < self.__toTreeBank.size():
            if self.__fromTreeBank.get(i).getName() < self.__toTreeBank.get(j).getName():
                self.__fromTreeBank.removeTree(i)
            elif self.__fromTreeBank.get(i).getName() > self.__toTreeBank.get(j).getName():
                self.__toTreeBank.removeTree(j)
            else:
                i = i + 1
                j = j + 1
        while i < self.__fromTreeBank.size():
            self.__fromTreeBank.removeTree(i)
        while j < self.__toTreeBank.size():
            self.__toTreeBank.removeTree(j)

    cpdef int size(self):
        return self.__fromTreeBank.size()

    cpdef ParseTreeDrawable fromTree(self, int index):
        return self.__fromTreeBank.get(index)

    cpdef ParseTreeDrawable toTree(self, int index):
        return self.__toTreeBank.get(index)

    cpdef TreeBankDrawable fromTreeBank(self):
        return self.__fromTreeBank

    cpdef TreeBankDrawable toTreeBank(self):
        return self.__toTreeBank
