
from radware.sdk.beans_common import *


class Icmp6StatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.IntfIndex = kwargs.get('IntfIndex', None)
        self.InMsgs = kwargs.get('InMsgs', None)
        self.InErrors = kwargs.get('InErrors', None)
        self.InEchos = kwargs.get('InEchos', None)
        self.InEchoReps = kwargs.get('InEchoReps', None)
        self.InNSs = kwargs.get('InNSs', None)
        self.InNAs = kwargs.get('InNAs', None)
        self.InRSs = kwargs.get('InRSs', None)
        self.InRAs = kwargs.get('InRAs', None)
        self.InDestUnreachs = kwargs.get('InDestUnreachs', None)
        self.InTimeExcds = kwargs.get('InTimeExcds', None)
        self.InTooBigs = kwargs.get('InTooBigs', None)
        self.InParmProbs = kwargs.get('InParmProbs', None)
        self.InRedirects = kwargs.get('InRedirects', None)
        self.OutMsgs = kwargs.get('OutMsgs', None)
        self.OutErrors = kwargs.get('OutErrors', None)
        self.OutEchos = kwargs.get('OutEchos', None)
        self.OutEchoReps = kwargs.get('OutEchoReps', None)
        self.OutNSs = kwargs.get('OutNSs', None)
        self.OutNAs = kwargs.get('OutNAs', None)
        self.OutRSs = kwargs.get('OutRSs', None)
        self.OutRAs = kwargs.get('OutRAs', None)
        self.OutRedirects = kwargs.get('OutRedirects', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

