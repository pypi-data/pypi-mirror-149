
from radware.sdk.beans_common import *


class BwmStatTcTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContractIndex = kwargs.get('ContractIndex', None)
        self.Name = kwargs.get('Name', None)
        self.Outoct = kwargs.get('Outoct', None)
        self.Outdisoct = kwargs.get('Outdisoct', None)
        self.BufferUsed = kwargs.get('BufferUsed', None)
        self.BufferMax = kwargs.get('BufferMax', None)
        self.TotalPackets = kwargs.get('TotalPackets', None)
        self.SessRejected = kwargs.get('SessRejected', None)

    def get_indexes(self):
        return self.ContractIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ContractIndex',

