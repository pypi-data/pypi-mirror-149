
from radware.sdk.beans_common import *


class EnumSlbSslCdpGrpDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewSslCfgSSLCdpGrpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.CdpGrpIdIndex = kwargs.get('CdpGrpIdIndex', None)
        self.CdpGrpDel = EnumSlbSslCdpGrpDel.enum(kwargs.get('CdpGrpDel', None))

    def get_indexes(self):
        return self.CdpGrpIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'CdpGrpIdIndex',

