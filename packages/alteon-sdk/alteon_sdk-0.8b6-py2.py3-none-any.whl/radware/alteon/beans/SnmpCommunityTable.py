
from radware.sdk.beans_common import *


class SnmpCommunityTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.SecurityName = kwargs.get('SecurityName', None)
        self.ContextEngineID = kwargs.get('ContextEngineID', None)
        self.ContextName = kwargs.get('ContextName', None)
        self.TransportTag = kwargs.get('TransportTag', None)
        self.StorageType = kwargs.get('StorageType', None)
        self.Status = kwargs.get('Status', None)   #RowStatus


    def get_indexes(self):
        return self.Index, 

    @classmethod
    def get_index_names(cls):
        return 'Index',

