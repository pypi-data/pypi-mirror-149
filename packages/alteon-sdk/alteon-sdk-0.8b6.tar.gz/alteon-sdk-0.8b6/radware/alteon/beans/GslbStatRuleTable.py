
from radware.sdk.beans_common import *


class GslbStatRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.Leastconns = kwargs.get('Leastconns', None)
        self.Roundrobin = kwargs.get('Roundrobin', None)
        self.Minmisses = kwargs.get('Minmisses', None)
        self.Hash = kwargs.get('Hash', None)
        self.Response = kwargs.get('Response', None)
        self.Geographical = kwargs.get('Geographical', None)
        self.Network = kwargs.get('Network', None)
        self.Random = kwargs.get('Random', None)
        self.Availability = kwargs.get('Availability', None)
        self.Qos = kwargs.get('Qos', None)
        self.Persistence = kwargs.get('Persistence', None)
        self.Local = kwargs.get('Local', None)
        self.Always = kwargs.get('Always', None)
        self.Remote = kwargs.get('Remote', None)
        self.Total = kwargs.get('Total', None)
        self.Phash = kwargs.get('Phash', None)
        self.AbsLeastconns = kwargs.get('AbsLeastconns', None)

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

