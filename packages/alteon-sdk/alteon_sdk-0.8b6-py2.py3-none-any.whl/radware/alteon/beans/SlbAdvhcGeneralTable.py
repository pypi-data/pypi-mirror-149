
from radware.sdk.beans_common import *


class SlbAdvhcGeneralTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Type = kwargs.get('Type', None)
        self.Name = kwargs.get('Name', None)
        self.DPort = kwargs.get('DPort', None)
        self.IPVer = kwargs.get('IPVer', None)
        self.HostName = kwargs.get('HostName', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

