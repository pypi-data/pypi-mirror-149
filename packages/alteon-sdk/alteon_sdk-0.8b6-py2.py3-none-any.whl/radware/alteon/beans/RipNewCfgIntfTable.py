
from radware.sdk.beans_common import *


class EnumRipIntfVersion(BaseBeanEnum):
    ripVersion1 = 1
    ripVersion2 = 2
    both = 3


class EnumRipIntfSupply(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfListen(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfTrigUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfMcastUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfPoisonReverse(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRipIntfAuth(BaseBeanEnum):
    none = 1
    password = 2


class EnumRipIntfDefault(BaseBeanEnum):
    both = 1
    listen = 2
    supply = 3
    none = 4


class RipNewCfgIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Version = EnumRipIntfVersion.enum(kwargs.get('Version', None))
        self.Supply = EnumRipIntfSupply.enum(kwargs.get('Supply', None))
        self.Listen = EnumRipIntfListen.enum(kwargs.get('Listen', None))
        self.TrigUpdate = EnumRipIntfTrigUpdate.enum(kwargs.get('TrigUpdate', None))
        self.McastUpdate = EnumRipIntfMcastUpdate.enum(kwargs.get('McastUpdate', None))
        self.PoisonReverse = EnumRipIntfPoisonReverse.enum(kwargs.get('PoisonReverse', None))
        self.State = EnumRipIntfState.enum(kwargs.get('State', None))
        self.Metric = kwargs.get('Metric', None)
        self.Auth = EnumRipIntfAuth.enum(kwargs.get('Auth', None))
        self.Key = kwargs.get('Key', None)
        self.Default = EnumRipIntfDefault.enum(kwargs.get('Default', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

