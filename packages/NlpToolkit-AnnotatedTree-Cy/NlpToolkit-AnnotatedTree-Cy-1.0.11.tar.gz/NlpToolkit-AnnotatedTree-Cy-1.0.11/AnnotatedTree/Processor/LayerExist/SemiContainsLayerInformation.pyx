from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode cimport IsTurkishLeafNode
from AnnotatedTree.Processor.LayerExist.LeafListCondition cimport LeafListCondition


cdef class ContainsLayerInformation(LeafListCondition):

    cdef object __viewLayerType

    def __init__(self, viewLayerType: ViewLayerType):
        self.__viewLayerType = viewLayerType

    cpdef bint satisfies(self, list leafList):
        cdef int notDone, done
        cdef ParseNodeDrawable parseNode
        notDone = 0
        done = 0
        for parseNode in leafList:
            if isinstance(parseNode, ParseNodeDrawable) and "*" \
                    not in parseNode.getLayerData(ViewLayerType.ENGLISH_WORD):
                if self.__viewLayerType == ViewLayerType.TURKISH_WORD:
                    if parseNode.getLayerData(self.__viewLayerType) is not None:
                        done = done + 1
                    else:
                        notDone = notDone + 1
                elif self.__viewLayerType == ViewLayerType.PART_OF_SPEECH or \
                        self.__viewLayerType == ViewLayerType.INFLECTIONAL_GROUP or \
                        self.__viewLayerType == ViewLayerType.NER or self.__viewLayerType == ViewLayerType.SEMANTICS or\
                        self.__viewLayerType == ViewLayerType.PROPBANK:
                    if IsTurkishLeafNode().satisfies(parseNode):
                        if parseNode.getLayerData(self.__viewLayerType) is not None:
                            done = done + 1
                        else:
                            notDone = notDone + 1
        return done != 0 and notDone != 0
