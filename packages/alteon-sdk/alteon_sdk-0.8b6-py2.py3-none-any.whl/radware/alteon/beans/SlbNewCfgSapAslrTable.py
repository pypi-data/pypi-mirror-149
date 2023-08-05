
from radware.sdk.beans_common import *


class EnumSlbSapAslrIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbSapAslrVipIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbSapAslrState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSapAslrAutoConfig(BaseBeanEnum):
    basic = 1
    full = 2


class EnumSlbSapAslrDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgSapAslrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.IpVer = EnumSlbSapAslrIpVer.enum(kwargs.get('IpVer', None))
        self.PortNum = kwargs.get('PortNum', None)
        self.VipAddr = kwargs.get('VipAddr', None)
        self.Vipv6Addr = kwargs.get('Vipv6Addr', None)
        self.VipIpVer = EnumSlbSapAslrVipIpVer.enum(kwargs.get('VipIpVer', None))
        self.Interval = kwargs.get('Interval', None)
        self.State = EnumSlbSapAslrState.enum(kwargs.get('State', None))
        self.Name = kwargs.get('Name', None)
        self.LastAct = kwargs.get('LastAct', None)
        self.AutoConfig = EnumSlbSapAslrAutoConfig.enum(kwargs.get('AutoConfig', None))
        self.SessionInfo = kwargs.get('SessionInfo', None)
        self.Delete = EnumSlbSapAslrDelete.enum(kwargs.get('Delete', None))
        self.Signature = kwargs.get('Signature', None)
        self.ServCert = kwargs.get('ServCert', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

