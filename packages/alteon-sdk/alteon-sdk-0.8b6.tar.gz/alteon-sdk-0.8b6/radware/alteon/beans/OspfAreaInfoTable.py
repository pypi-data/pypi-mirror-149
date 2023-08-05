
from radware.sdk.beans_common import *


class OspfAreaInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.TotalNumberOfInterfaces = kwargs.get('TotalNumberOfInterfaces', None)
        self.NumberOfInterfacesUp = kwargs.get('NumberOfInterfacesUp', None)
        self.NumberOfLsdbEntries = kwargs.get('NumberOfLsdbEntries', None)
        self.Id = kwargs.get('Id', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

