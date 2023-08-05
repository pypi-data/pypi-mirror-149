
from radware.sdk.beans_common import *


class EnumSlbUrlBwmDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgUrlBwmTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.UrlId = kwargs.get('UrlId', None)
        self.Contract = kwargs.get('Contract', None)
        self.Delete = EnumSlbUrlBwmDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex, self.UrlId,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex', 'UrlId',

