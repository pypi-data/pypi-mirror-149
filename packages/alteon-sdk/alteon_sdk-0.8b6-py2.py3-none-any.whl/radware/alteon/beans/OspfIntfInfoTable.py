
from radware.sdk.beans_common import *


class OspfIntfInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IfInfoIndex = kwargs.get('IfInfoIndex', None)
        self.IfDesignatedRouterIP = kwargs.get('IfDesignatedRouterIP', None)
        self.IfBackupDesignatedRouterIP = kwargs.get('IfBackupDesignatedRouterIP', None)
        self.IfWaitInterval = kwargs.get('IfWaitInterval', None)
        self.IfTotalNeighbours = kwargs.get('IfTotalNeighbours', None)
        self.IfInfoIpAddress = kwargs.get('IfInfoIpAddress', None)

    def get_indexes(self):
        return self.IfInfoIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IfInfoIndex',

