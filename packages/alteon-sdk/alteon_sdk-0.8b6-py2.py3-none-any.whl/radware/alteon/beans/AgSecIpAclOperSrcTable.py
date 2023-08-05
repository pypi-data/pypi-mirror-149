
from radware.sdk.beans_common import *


class AgSecIpAclOperSrcTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListSrcIndx = kwargs.get('ListSrcIndx', None)
        self.ListSrcAddr = kwargs.get('ListSrcAddr', None)
        self.ListSrcMask = kwargs.get('ListSrcMask', None)
        self.ListSrcTimeOut = kwargs.get('ListSrcTimeOut', None)

    def get_indexes(self):
        return self.ListSrcIndx,
    
    @classmethod
    def get_index_names(cls):
        return 'ListSrcIndx',

