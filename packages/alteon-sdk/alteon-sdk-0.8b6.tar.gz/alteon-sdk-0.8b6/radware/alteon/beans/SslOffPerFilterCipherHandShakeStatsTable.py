
from radware.sdk.beans_common import *


class SslOffPerFilterCipherHandShakeStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.FiltId = kwargs.get('FiltId', None)
        self.ByCipherHandShakeCipherName = kwargs.get('ByCipherHandShakeCipherName', None)
        self.ByCipherHandShakeCipherHits = kwargs.get('ByCipherHandShakeCipherHits', None)
        self.ByCipherHandShakeCipherHitsTotal = kwargs.get('ByCipherHandShakeCipherHitsTotal', None)

    def get_indexes(self):
        return self.FiltId, self.ByCipherHandShakeCipherName,
    
    @classmethod
    def get_index_names(cls):
        return 'FiltId', 'ByCipherHandShakeCipherName',

