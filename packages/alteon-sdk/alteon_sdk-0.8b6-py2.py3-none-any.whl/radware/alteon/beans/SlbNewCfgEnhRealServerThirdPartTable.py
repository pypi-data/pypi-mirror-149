
from radware.sdk.beans_common import *


class SlbNewCfgEnhRealServerThirdPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Oid = kwargs.get('Oid', None)
        self.CommString = kwargs.get('CommString', None)
        self.BackUp = kwargs.get('BackUp', None)
        self.HealthID = kwargs.get('HealthID', None)
        self.CriticalConnThrsh = kwargs.get('CriticalConnThrsh', None)
        self.HighConnThrsh = kwargs.get('HighConnThrsh', None)
        self.UploadBandWidth = kwargs.get('UploadBandWidth', None)
        self.DownloadBandWidth = kwargs.get('DownloadBandWidth', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

