
from radware.sdk.beans_common import *


class Dot1dBasePortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Port = kwargs.get('Port', None)
        self.IfIndex = kwargs.get('IfIndex', None)
        self.Circuit = kwargs.get('Circuit', None)
        self.DelayExceededDiscards = kwargs.get('DelayExceededDiscards', None)
        self.MtuExceededDiscards = kwargs.get('MtuExceededDiscards', None)

    def get_indexes(self):
        return self.Port,
    
    @classmethod
    def get_index_names(cls):
        return 'Port',

