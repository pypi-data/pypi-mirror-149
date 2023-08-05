
from radware.sdk.beans_common import *


class EnumGslbOperDnsSecEmergencyRollover(BaseBeanEnum):
    other = 1
    rollover = 2


class EnumGslbOperDnsSecImmediateRollover(BaseBeanEnum):
    other = 1
    rollover = 2


class GslbOperDnsSecTable(DeviceBean):
    def __init__(self, **kwargs):
        self.KeyID = kwargs.get('KeyID', None)
        self.EmergencyRollover = EnumGslbOperDnsSecEmergencyRollover.enum(kwargs.get('EmergencyRollover', None))
        self.ImmediateRollover = EnumGslbOperDnsSecImmediateRollover.enum(kwargs.get('ImmediateRollover', None))

    def get_indexes(self):
        return self.KeyID,
    
    @classmethod
    def get_index_names(cls):
        return 'KeyID',

