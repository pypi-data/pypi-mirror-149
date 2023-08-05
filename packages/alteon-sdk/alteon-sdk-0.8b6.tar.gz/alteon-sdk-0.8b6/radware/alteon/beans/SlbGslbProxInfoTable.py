
from radware.sdk.beans_common import *


class SlbGslbProxInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SubnetIndex = kwargs.get('SubnetIndex', None)
        self.SubnetIp = kwargs.get('SubnetIp', None)
        self.NhrRank1 = kwargs.get('NhrRank1', None)
        self.NhrRank2 = kwargs.get('NhrRank2', None)
        self.NhrRank3 = kwargs.get('NhrRank3', None)
        self.NhrRTT1 = kwargs.get('NhrRTT1', None)
        self.NhrRTT2 = kwargs.get('NhrRTT2', None)
        self.NhrRTT3 = kwargs.get('NhrRTT3', None)
        self.NhrHOP1 = kwargs.get('NhrHOP1', None)
        self.NhrHOP2 = kwargs.get('NhrHOP2', None)
        self.NhrHOP3 = kwargs.get('NhrHOP3', None)
        self.NhrAge = kwargs.get('NhrAge', None)

    def get_indexes(self):
        return self.SubnetIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SubnetIndex',

