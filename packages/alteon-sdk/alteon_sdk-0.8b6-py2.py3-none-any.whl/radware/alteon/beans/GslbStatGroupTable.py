
from radware.sdk.beans_common import *


class GslbStatGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.DnsHandoffs = kwargs.get('DnsHandoffs', None)
        self.HttpRedirs = kwargs.get('HttpRedirs', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

