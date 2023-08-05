
from radware.sdk.beans_common import *


class AgSyslogMsgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Message = kwargs.get('Message', None)
        self.MessageDate = kwargs.get('MessageDate', None)
        self.MessageSeverity = kwargs.get('MessageSeverity', None)
        self.MessageOnly = kwargs.get('MessageOnly', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

