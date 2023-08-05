
from radware.sdk.beans_common import *


class OspfAreaNbrChangeStats(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Nbrhello = kwargs.get('Nbrhello', None)
        self.Start = kwargs.get('Start', None)
        self.AdjointOk = kwargs.get('AdjointOk', None)
        self.NegotiationDone = kwargs.get('NegotiationDone', None)
        self.ExchangeDone = kwargs.get('ExchangeDone', None)
        self.BadRequests = kwargs.get('BadRequests', None)
        self.BadSequence = kwargs.get('BadSequence', None)
        self.LoadingDone = kwargs.get('LoadingDone', None)
        self.N1way = kwargs.get('N1way', None)
        self.RstAd = kwargs.get('RstAd', None)
        self.Down = kwargs.get('Down', None)
        self.N2way = kwargs.get('N2way', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

