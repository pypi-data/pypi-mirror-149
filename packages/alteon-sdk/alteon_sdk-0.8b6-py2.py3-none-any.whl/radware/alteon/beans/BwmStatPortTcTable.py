
from radware.sdk.beans_common import *


class BwmStatPortTcTable(DeviceBean):
    def __init__(self, **kwargs):
        self.PortIndex = kwargs.get('PortIndex', None)
        self.ContractIndex = kwargs.get('ContractIndex', None)
        self.Name = kwargs.get('Name', None)
        self.Outoct = kwargs.get('Outoct', None)
        self.Outdisoct = kwargs.get('Outdisoct', None)
        self.BufferUsed = kwargs.get('BufferUsed', None)
        self.BufferMax = kwargs.get('BufferMax', None)
        self.TotalPackets = kwargs.get('TotalPackets', None)

    def get_indexes(self):
        return self.PortIndex, self.ContractIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'PortIndex', 'ContractIndex',

