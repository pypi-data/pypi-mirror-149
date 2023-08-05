cdef class SingleWordMultiItemLayer(SingleWordLayer):

    cpdef object getItemAt(self, int index):
        if index < len(self.items):
            return self.items[index]
        else:
            return None

    cpdef getLayerSize(self, object viewLayer):
        return len(self.items)
