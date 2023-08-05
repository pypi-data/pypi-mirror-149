
from radware.sdk.beans_common import *


class BwmAvailableContractsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContractIndx = kwargs.get('ContractIndx', None)
        self.ContractName = kwargs.get('ContractName', None)

    def get_indexes(self):
        return self.ContractIndx,
    
    @classmethod
    def get_index_names(cls):
        return 'ContractIndx',

