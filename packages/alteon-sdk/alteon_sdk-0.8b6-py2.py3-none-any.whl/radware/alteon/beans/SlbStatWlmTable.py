
from radware.sdk.beans_common import *


class SlbStatWlmTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.RegReq = kwargs.get('RegReq', None)
        self.RegRep = kwargs.get('RegRep', None)
        self.RegRepErr = kwargs.get('RegRepErr', None)
        self.DeregReq = kwargs.get('DeregReq', None)
        self.DeregRep = kwargs.get('DeregRep', None)
        self.DeregRepErr = kwargs.get('DeregRepErr', None)
        self.LbStateReq = kwargs.get('LbStateReq', None)
        self.LbStateRep = kwargs.get('LbStateRep', None)
        self.LbStateRepErr = kwargs.get('LbStateRepErr', None)
        self.MembStateReq = kwargs.get('MembStateReq', None)
        self.MembStateRep = kwargs.get('MembStateRep', None)
        self.MembStateRepErr = kwargs.get('MembStateRepErr', None)
        self.WtMsgRecv = kwargs.get('WtMsgRecv', None)
        self.WtMsgParErr = kwargs.get('WtMsgParErr', None)
        self.TotInvalidLb = kwargs.get('TotInvalidLb', None)
        self.TotInvalidGrp = kwargs.get('TotInvalidGrp', None)
        self.TotInvalidRealSer = kwargs.get('TotInvalidRealSer', None)
        self.MsgInvalidSASPHeader = kwargs.get('MsgInvalidSASPHeader', None)
        self.MsgParseErr = kwargs.get('MsgParseErr', None)
        self.MsgUnsupMsgType = kwargs.get('MsgUnsupMsgType', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

