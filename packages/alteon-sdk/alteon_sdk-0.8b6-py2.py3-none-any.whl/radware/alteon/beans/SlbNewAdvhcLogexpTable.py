
from radware.sdk.beans_common import *


class SlbNewAdvhcLogexpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Text = kwargs.get('Text', None)
        self.Copy = kwargs.get('Copy', None)
        self.Delete = kwargs.get('Delete', None)
        self.Always = kwargs.get('Always', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

