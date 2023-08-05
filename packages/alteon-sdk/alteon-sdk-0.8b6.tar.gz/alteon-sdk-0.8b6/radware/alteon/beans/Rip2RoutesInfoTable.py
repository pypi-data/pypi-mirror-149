
from radware.sdk.beans_common import *


class Rip2RoutesInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.DestIndex = kwargs.get('DestIndex', None)
        self.NxtHopIndex = kwargs.get('NxtHopIndex', None)
        self.Destination = kwargs.get('Destination', None)
        self.IpAddress = kwargs.get('IpAddress', None)
        self.Metric = kwargs.get('Metric', None)

    def get_indexes(self):
        return self.DestIndex, self.NxtHopIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'DestIndex', 'NxtHopIndex',

