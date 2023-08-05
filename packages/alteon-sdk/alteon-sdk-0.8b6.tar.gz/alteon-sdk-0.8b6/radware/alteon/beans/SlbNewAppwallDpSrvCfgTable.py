
from radware.sdk.beans_common import *


class EnumSlbAppwallDpSrvDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAppwallDpSrvCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.DpSrvId = kwargs.get('DpSrvId', None)
        self.DpSrvIpAddress = kwargs.get('DpSrvIpAddress', None)
        self.DpSrvPort = kwargs.get('DpSrvPort', None)
        self.DpSrvDel = EnumSlbAppwallDpSrvDel.enum(kwargs.get('DpSrvDel', None))

    def get_indexes(self):
        return self.DpSrvId,
    
    @classmethod
    def get_index_names(cls):
        return 'DpSrvId',

