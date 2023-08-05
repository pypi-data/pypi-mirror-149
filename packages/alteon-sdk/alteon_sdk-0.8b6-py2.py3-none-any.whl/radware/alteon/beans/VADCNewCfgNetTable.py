
from radware.sdk.beans_common import *


class EnumVADCNetIPver(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class EnumVADCNetRemId(BaseBeanEnum):
    other = 1
    delete = 2


class VADCNewCfgNetTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.VlanId = kwargs.get('VlanId', None)
        self.IPver = EnumVADCNetIPver.enum(kwargs.get('IPver', None))
        self.IPBegin = kwargs.get('IPBegin', None)
        self.Mask = kwargs.get('Mask', None)
        self.IPEnd = kwargs.get('IPEnd', None)
        self.RemId = EnumVADCNetRemId.enum(kwargs.get('RemId', None))
        self.IPv6Begin = kwargs.get('IPv6Begin', None)
        self.Prefix = kwargs.get('Prefix', None)
        self.IPv6End = kwargs.get('IPv6End', None)
        self.VADCId = kwargs.get('VADCId', None)

    def get_indexes(self):
        return self.VADCId, self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId', 'Id',

