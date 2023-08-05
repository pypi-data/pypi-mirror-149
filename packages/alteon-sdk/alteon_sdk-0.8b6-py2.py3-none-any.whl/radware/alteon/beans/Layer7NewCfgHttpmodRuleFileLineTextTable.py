
from radware.sdk.beans_common import *


class Layer7NewCfgHttpmodRuleFileLineTextTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.TypRep = kwargs.get('TypRep', None)
        self.TypNew = kwargs.get('TypNew', None)
        self.StatlineCode = kwargs.get('StatlineCode', None)
        self.StatlineTxt = kwargs.get('StatlineTxt', None)
        self.StatlineNewCode = kwargs.get('StatlineNewCode', None)
        self.StatlineNewTxt = kwargs.get('StatlineNewTxt', None)
        self.TextReplace = kwargs.get('TextReplace', None)
        self.TextNewText = kwargs.get('TextNewText', None)
        self.TextRemove = kwargs.get('TextRemove', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

