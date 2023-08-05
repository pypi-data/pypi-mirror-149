
from radware.sdk.beans_common import *


class SlbAppShapeStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ScriptId = kwargs.get('ScriptId', None)
        self.Event = kwargs.get('Event', None)
        self.Activations = kwargs.get('Activations', None)
        self.Failures = kwargs.get('Failures', None)
        self.Aborts = kwargs.get('Aborts', None)
        self.EventAsString = kwargs.get('EventAsString', None)

    def get_indexes(self):
        return self.ScriptId,
    
    @classmethod
    def get_index_names(cls):
        return 'ScriptId',

