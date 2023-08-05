
from radware.sdk.beans_common import *


class EnumGslbRuleState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbRuleType(BaseBeanEnum):
    gslb = 0
    inboundllb = 1


class EnumGslbRuleEdnsPrst(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbRulePersist(BaseBeanEnum):
    domain = 1
    ip = 2


class EnumGslbRuleNetworkFallback(BaseBeanEnum):
    enabled = 1
    disabled = 2


class GslbNewCfgRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.State = EnumGslbRuleState.enum(kwargs.get('State', None))
        self.StartHour = kwargs.get('StartHour', None)
        self.StartMin = kwargs.get('StartMin', None)
        self.EndHour = kwargs.get('EndHour', None)
        self.EndMin = kwargs.get('EndMin', None)
        self.TTL = kwargs.get('TTL', None)
        self.RR = kwargs.get('RR', None)
        self.Dname = kwargs.get('Dname', None)
        self.Delete = EnumGslbRuleDelete.enum(kwargs.get('Delete', None))
        self.IpNetMask = kwargs.get('IpNetMask', None)
        self.Timeout = kwargs.get('Timeout', None)
        self.Ipv6Prefix = kwargs.get('Ipv6Prefix', None)
        self.Type = EnumGslbRuleType.enum(kwargs.get('Type', None))
        self.Name = kwargs.get('Name', None)
        self.Port = kwargs.get('Port', None)
        self.EdnsPrst = EnumGslbRuleEdnsPrst.enum(kwargs.get('EdnsPrst', None))
        self.Persist = EnumGslbRulePersist.enum(kwargs.get('Persist', None))
        self.NetworkFallback = EnumGslbRuleNetworkFallback.enum(kwargs.get('NetworkFallback', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

