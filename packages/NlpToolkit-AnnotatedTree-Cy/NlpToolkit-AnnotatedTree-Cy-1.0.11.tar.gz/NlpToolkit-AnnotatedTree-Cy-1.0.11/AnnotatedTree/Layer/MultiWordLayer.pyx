cdef class MultiWordLayer(WordLayer):

    cpdef object getItemAt(self, int index):
        if index < len(self.items):
            return self.items[index]
        else:
            return None

    cpdef int size(self):
        return len(self.items)

    cpdef setLayerValue(self, str layerValue):
        pass
