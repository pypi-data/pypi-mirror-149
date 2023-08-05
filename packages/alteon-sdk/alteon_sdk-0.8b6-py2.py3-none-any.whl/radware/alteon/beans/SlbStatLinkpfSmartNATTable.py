
from radware.sdk.beans_common import *


class EnumSlbStatLinkpfSmartNATType(BaseBeanEnum):
    nonat = 0
    static = 1
    dynamic = 2


class SlbStatLinkpfSmartNATTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NATIndex = kwargs.get('NATIndex', None)
        self.NATCurrSess = kwargs.get('NATCurrSess', None)
        self.NATTotSess = kwargs.get('NATTotSess', None)
        self.NATType = EnumSlbStatLinkpfSmartNATType.enum(kwargs.get('NATType', None))

    def get_indexes(self):
        return self.NATIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NATIndex',

