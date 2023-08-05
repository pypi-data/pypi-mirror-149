
from radware.sdk.beans_common import *


class EnumBwmPolicyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumBwmPolicyType(BaseBeanEnum):
    throughput = 1
    pps = 2


class BwmNewCfgPolicyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.TosIn = kwargs.get('TosIn', None)
        self.TosOut = kwargs.get('TosOut', None)
        self.Hard = kwargs.get('Hard', None)
        self.Soft = kwargs.get('Soft', None)
        self.Resv = kwargs.get('Resv', None)
        self.Buffer = kwargs.get('Buffer', None)
        self.Delete = EnumBwmPolicyDelete.enum(kwargs.get('Delete', None))
        self.UserLimit = kwargs.get('UserLimit', None)
        self.Type = EnumBwmPolicyType.enum(kwargs.get('Type', None))
        self.HardPPS = kwargs.get('HardPPS', None)
        self.UserPPS = kwargs.get('UserPPS', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

