
from radware.sdk.beans_common import *


class SlbStatPipNwClassTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.Used = kwargs.get('Used', None)
        self.Failure = kwargs.get('Failure', None)

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

