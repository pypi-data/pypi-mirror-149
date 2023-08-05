
from radware.sdk.beans_common import *


class EnumRipInfoIntfVersion(BaseBeanEnum):
    ripVersion1 = 1
    ripVersion2 = 2


class EnumRipInfoIntfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfListen(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfTrigUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfMcastUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfPoisonReverse(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfSupply(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipInfoIntfAuth(BaseBeanEnum):
    none = 1
    password = 2


class EnumRipInfoIntfDefault(BaseBeanEnum):
    both = 1
    listen = 2
    supply = 3
    none = 4


class Rip2InfoIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Version = EnumRipInfoIntfVersion.enum(kwargs.get('Version', None))
        self.Address = kwargs.get('Address', None)
        self.State = EnumRipInfoIntfState.enum(kwargs.get('State', None))
        self.Listen = EnumRipInfoIntfListen.enum(kwargs.get('Listen', None))
        self.TrigUpdate = EnumRipInfoIntfTrigUpdate.enum(kwargs.get('TrigUpdate', None))
        self.McastUpdate = EnumRipInfoIntfMcastUpdate.enum(kwargs.get('McastUpdate', None))
        self.PoisonReverse = EnumRipInfoIntfPoisonReverse.enum(kwargs.get('PoisonReverse', None))
        self.Supply = EnumRipInfoIntfSupply.enum(kwargs.get('Supply', None))
        self.Metric = kwargs.get('Metric', None)
        self.Auth = EnumRipInfoIntfAuth.enum(kwargs.get('Auth', None))
        self.Key = kwargs.get('Key', None)
        self.Default = EnumRipInfoIntfDefault.enum(kwargs.get('Default', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

