
from radware.sdk.beans_common import *


class IpAclBogonInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Ip = kwargs.get('Ip', None)
        self.Mask = kwargs.get('Mask', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

