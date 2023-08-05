
from radware.sdk.beans_common import *


class EnumSlbSslSSLInspectFlowSeGroupState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumSlbSslSSLInspectFlowSeGroupFallback(BaseBeanEnum):
    none = 1
    continue_ = 2
    drop = 3


class EnumSlbSslSSLInspectFlowDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewSslCfgSSLInspectFlowTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.SeGroupIndex = kwargs.get('SeGroupIndex', None)
        self.SeGroupState = EnumSlbSslSSLInspectFlowSeGroupState.enum(kwargs.get('SeGroupState', None))
        self.SeGroupLocation = kwargs.get('SeGroupLocation', None)
        self.SeGroupFallback = EnumSlbSslSSLInspectFlowSeGroupFallback.enum(kwargs.get('SeGroupFallback', None))
        self.SeGroupRedFiltId = kwargs.get('SeGroupRedFiltId', None)
        self.GroupID = kwargs.get('GroupID', None)
        self.Delete = EnumSlbSslSSLInspectFlowDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index, self.SeGroupIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'SeGroupIndex',

