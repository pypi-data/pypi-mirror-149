
from radware.sdk.beans_common import *


class AgSyslogSavedMsgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.MsgSavedIndex = kwargs.get('MsgSavedIndex', None)
        self.Message = kwargs.get('Message', None)

    def get_indexes(self):
        return self.MsgSavedIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'MsgSavedIndex',

