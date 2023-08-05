
from radware.sdk.beans_common import *


class EnumSlbTcpPolRcvWndSize(BaseBeanEnum):
    sz128K = 0
    sz256K = 1
    sz512K = 2
    sz1M = 3
    sz2M = 4
    sz3M = 5
    sz4M = 6


class EnumSlbTcpPolSndWndSize(BaseBeanEnum):
    sz128K = 0
    sz256K = 1
    sz512K = 2
    sz1M = 3
    sz2M = 4
    sz3M = 5
    sz4M = 6


class EnumSlbTcpPolMss(BaseBeanEnum):
    def_ = 0
    sz1460 = 1
    sz1440 = 2
    sz1360 = 3
    sz1212 = 4
    sz956 = 5
    sz536 = 6
    sz384 = 7
    sz128 = 8
    sz1400 = 9


class EnumSlbTcpPolCaAlgorithm(BaseBeanEnum):
    reno = 0
    hybla = 1
    hyblaAndPacing = 2
    westwood = 3


class EnumSlbTcpPolAdaptiveTuning(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbTcpPolSelAck(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbTcpPolState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbTcpPolDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbTcpPolImmediateAck(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbTcpPolNagle(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewTcpPolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.RcvWndSize = EnumSlbTcpPolRcvWndSize.enum(kwargs.get('RcvWndSize', None))
        self.SndWndSize = EnumSlbTcpPolSndWndSize.enum(kwargs.get('SndWndSize', None))
        self.Mss = EnumSlbTcpPolMss.enum(kwargs.get('Mss', None))
        self.CaAlgorithm = EnumSlbTcpPolCaAlgorithm.enum(kwargs.get('CaAlgorithm', None))
        self.AdaptiveTuning = EnumSlbTcpPolAdaptiveTuning.enum(kwargs.get('AdaptiveTuning', None))
        self.SelAck = EnumSlbTcpPolSelAck.enum(kwargs.get('SelAck', None))
        self.State = EnumSlbTcpPolState.enum(kwargs.get('State', None))
        self.Del = EnumSlbTcpPolDel.enum(kwargs.get('Del', None))
        self.ReadBufferSize = kwargs.get('ReadBufferSize', None)
        self.CaScale = kwargs.get('CaScale', None)
        self.CaDecrease = kwargs.get('CaDecrease', None)
        self.ImmediateAck = EnumSlbTcpPolImmediateAck.enum(kwargs.get('ImmediateAck', None))
        self.Nagle = EnumSlbTcpPolNagle.enum(kwargs.get('Nagle', None))
        self.Finage = kwargs.get('Finage', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

