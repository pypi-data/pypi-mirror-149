
from radware.sdk.beans_common import *


class EnumLayer7HttpmodRuleHdrElmnt(BaseBeanEnum):
    url = 1
    header = 2
    cookie = 3
    filetype = 4
    statusline = 5
    text = 6
    regex = 7
    none = 8


class Layer7NewCfgHttpmodRuleHdrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Insert = kwargs.get('Insert', None)
        self.Value = kwargs.get('Value', None)
        self.Elmnt = EnumLayer7HttpmodRuleHdrElmnt.enum(kwargs.get('Elmnt', None))
        self.ElmntUrlHost = kwargs.get('ElmntUrlHost', None)
        self.ElmntUrlPath = kwargs.get('ElmntUrlPath', None)
        self.ElmntHdrField = kwargs.get('ElmntHdrField', None)
        self.ElmntHdrVal = kwargs.get('ElmntHdrVal', None)
        self.ElmntCookey = kwargs.get('ElmntCookey', None)
        self.ElmntCkieVal = kwargs.get('ElmntCkieVal', None)
        self.ElmntFileTyp = kwargs.get('ElmntFileTyp', None)
        self.ElmntStatusCode = kwargs.get('ElmntStatusCode', None)
        self.ElmntStatusTxt = kwargs.get('ElmntStatusTxt', None)
        self.ElmntTxt = kwargs.get('ElmntTxt', None)
        self.ElmntRegx = kwargs.get('ElmntRegx', None)
        self.ReplacHdr = kwargs.get('ReplacHdr', None)
        self.ReplacVal = kwargs.get('ReplacVal', None)
        self.ReplacNewHdr = kwargs.get('ReplacNewHdr', None)
        self.ReplacNewVal = kwargs.get('ReplacNewVal', None)
        self.RemvHdr = kwargs.get('RemvHdr', None)
        self.RemvVal = kwargs.get('RemvVal', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

