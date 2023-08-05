cdef class LeafToLanguageConverter(LeafToStringConverter):

    cpdef str leafConverter(self, ParseNodeDrawable leafNode):
        cdef str layerData, parentLayerData
        layerData = leafNode.getLayerData(self.viewLayerType)
        parentLayerData = leafNode.getParent().getLayerData(self.viewLayerType)
        if layerData is not None:
            if "*" in layerData or (layerData == "0" and parentLayerData == "-NONE-"):
                return ""
            else:
                return " " + layerData.replace("-LRB-", "(").replace("-RRB-", ")").replace("-LSB-", "[").\
                    replace("-RSB-", "]").replace("-LCB-", "{").replace("-RCB-", "}").replace("-lrb-", "(").\
                    replace("-rrb-", ")").replace("-lsb-", "[").replace("-rsb-", "]").replace("-lcb", "{").\
                    replace("-rcb-", "}")
        else:
            return ""
