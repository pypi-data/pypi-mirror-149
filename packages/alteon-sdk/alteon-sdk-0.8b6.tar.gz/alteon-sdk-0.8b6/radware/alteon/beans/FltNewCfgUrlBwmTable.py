
from radware.sdk.beans_common import *


class EnumFltUrlBwmDelete(BaseBeanEnum):
    other = 1
    delete = 2


class FltNewCfgUrlBwmTable(DeviceBean):
    def __init__(self, **kwargs):
        self.FltIndex = kwargs.get('FltIndex', None)
        self.UrlId = kwargs.get('UrlId', None)
        self.Contract = kwargs.get('Contract', None)
        self.Delete = EnumFltUrlBwmDelete.enum(kwargs.get('Delete', None))
        self.ReverseBwmContract = kwargs.get('ReverseBwmContract', None)

    def get_indexes(self):
        return self.FltIndex, self.UrlId,
    
    @classmethod
    def get_index_names(cls):
        return 'FltIndex', 'UrlId',

