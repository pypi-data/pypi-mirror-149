
from radware.sdk.beans_common import *


class EnumSlbSslSSLCdpEntryDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewSslCfgSSLCdpEntryTable(DeviceBean):
    def __init__(self, **kwargs):
        self.GrpIdIndex = kwargs.get('GrpIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.URL = kwargs.get('URL', None)
        self.User = kwargs.get('User', None)
        self.Password = kwargs.get('Password', None)
        self.Delete = EnumSlbSslSSLCdpEntryDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.GrpIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'GrpIdIndex', 'Index',

