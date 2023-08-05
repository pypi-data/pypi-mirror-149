
from radware.sdk.beans_common import *


class EnumLayer7HttpmodRuleCookieInsrtElem(BaseBeanEnum):
    url = 1
    header = 2
    cookie = 3
    filetype = 4
    statusline = 5
    text = 6
    regex = 7
    none = 8


class Layer7NewCfgHttpmodRuleCookieTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.InsrtKey = kwargs.get('InsrtKey', None)
        self.InsrtVal = kwargs.get('InsrtVal', None)
        self.InsrtPath = kwargs.get('InsrtPath', None)
        self.InsrtDomn = kwargs.get('InsrtDomn', None)
        self.InsrtExp = kwargs.get('InsrtExp', None)
        self.InsrtElem = EnumLayer7HttpmodRuleCookieInsrtElem.enum(kwargs.get('InsrtElem', None))
        self.InsrtUrlHost = kwargs.get('InsrtUrlHost', None)
        self.InsrtUrlPath = kwargs.get('InsrtUrlPath', None)
        self.InsrtHdrFld = kwargs.get('InsrtHdrFld', None)
        self.InsrtHdrVal = kwargs.get('InsrtHdrVal', None)
        self.InsrtCookey = kwargs.get('InsrtCookey', None)
        self.InsrtCookieVal = kwargs.get('InsrtCookieVal', None)
        self.InsrtFiletyp = kwargs.get('InsrtFiletyp', None)
        self.InsrtStatsCode = kwargs.get('InsrtStatsCode', None)
        self.InsrtStatsTxt = kwargs.get('InsrtStatsTxt', None)
        self.InsrtTxt = kwargs.get('InsrtTxt', None)
        self.InsrtRegx = kwargs.get('InsrtRegx', None)
        self.ReplcCookey = kwargs.get('ReplcCookey', None)
        self.ReplcVal = kwargs.get('ReplcVal', None)
        self.ReplcNewKey = kwargs.get('ReplcNewKey', None)
        self.ReplcNewVal = kwargs.get('ReplcNewVal', None)
        self.RemvCookey = kwargs.get('RemvCookey', None)
        self.RemvCookieVal = kwargs.get('RemvCookieVal', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

