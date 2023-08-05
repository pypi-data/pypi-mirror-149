
from radware.sdk.beans_common import *


class EnumGslbMetricMetric(BaseBeanEnum):
    leastconns = 1
    roundrobin = 2
    response = 3
    geographical = 4
    network = 5
    random = 6
    availability = 7
    qos = 8
    minmisses = 9
    hash = 10
    local = 11
    always = 12
    remote = 13
    none = 14
    persistence = 15
    phash = 16
    proximity = 17
    bandwidth = 18
    absleastconns = 19


class GslbNewCfgMetricTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RuleMetricIndx = kwargs.get('RuleMetricIndx', None)
        self.Indx = kwargs.get('Indx', None)
        self.Metric = EnumGslbMetricMetric.enum(kwargs.get('Metric', None))
        self.NetworkBmap = kwargs.get('NetworkBmap', None)
        self.AddNetwork = kwargs.get('AddNetwork', None)
        self.RemNetwork = kwargs.get('RemNetwork', None)

    def get_indexes(self):
        return self.RuleMetricIndx, self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'RuleMetricIndx', 'Indx',

