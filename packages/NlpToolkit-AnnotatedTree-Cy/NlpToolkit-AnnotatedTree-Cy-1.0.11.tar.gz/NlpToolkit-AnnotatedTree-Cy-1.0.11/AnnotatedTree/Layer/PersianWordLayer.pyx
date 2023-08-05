from AnnotatedTree.Layer.TargetLanguageWordLayer cimport TargetLanguageWordLayer


cdef class PersianWordLayer(TargetLanguageWordLayer):

    def __init__(self, layerValue: str):
        super().__init__(layerValue)
        self.layerName = "persian"
