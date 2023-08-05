
from radware.sdk.beans_common import *


class FastviewEnhPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.WebappId = kwargs.get('WebappId', None)
        self.Transactions = kwargs.get('Transactions', None)
        self.Pages = kwargs.get('Pages', None)
        self.OptimizedPages = kwargs.get('OptimizedPages', None)
        self.LearningPages = kwargs.get('LearningPages', None)
        self.TokensParsed = kwargs.get('TokensParsed', None)
        self.TokensRewritten = kwargs.get('TokensRewritten', None)
        self.BytesSavedImgReduction = kwargs.get('BytesSavedImgReduction', None)
        self.BytesBeforeImgReduction = kwargs.get('BytesBeforeImgReduction', None)
        self.BytesSavedPercent = kwargs.get('BytesSavedPercent', None)
        self.RespWithExpiryModified = kwargs.get('RespWithExpiryModified', None)
        self.ExpiryModifiedPercent = kwargs.get('ExpiryModifiedPercent', None)
        self.PeakTransactions = kwargs.get('PeakTransactions', None)
        self.PeakPages = kwargs.get('PeakPages', None)
        self.PeakOptimizedPages = kwargs.get('PeakOptimizedPages', None)
        self.PeakLearningPages = kwargs.get('PeakLearningPages', None)
        self.PeakTokensParsed = kwargs.get('PeakTokensParsed', None)
        self.PeakTokensRewritten = kwargs.get('PeakTokensRewritten', None)
        self.TotTransactions = kwargs.get('TotTransactions', None)
        self.TotPages = kwargs.get('TotPages', None)
        self.TotOptimizedPages = kwargs.get('TotOptimizedPages', None)
        self.TotLearningPages = kwargs.get('TotLearningPages', None)
        self.TotTokensParsed = kwargs.get('TotTokensParsed', None)
        self.TotTokensRewritten = kwargs.get('TotTokensRewritten', None)
        self.TotBytesSavedImgReduction = kwargs.get('TotBytesSavedImgReduction', None)
        self.TotBytesBeforeImgReduction = kwargs.get('TotBytesBeforeImgReduction', None)
        self.TotBytesSavedPercent = kwargs.get('TotBytesSavedPercent', None)
        self.TotRespWithExpiryModified = kwargs.get('TotRespWithExpiryModified', None)
        self.TotExpiryModifiedPercent = kwargs.get('TotExpiryModifiedPercent', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

