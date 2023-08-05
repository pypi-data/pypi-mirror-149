
from radware.sdk.beans_common import *


class VADCStatsAccelResourceTable(DeviceBean):
    def __init__(self, **kwargs):
        self.vADCIndex = kwargs.get('vADCIndex', None)
        self.vADCName = kwargs.get('vADCName', None)
        self.CompLimit = kwargs.get('CompLimit', None)
        self.CompUtil = kwargs.get('CompUtil', None)
        self.SSLLimit = kwargs.get('SSLLimit', None)
        self.SSLUtil = kwargs.get('SSLUtil', None)
        self.ApmLimit = kwargs.get('ApmLimit', None)
        self.ApmUtil = kwargs.get('ApmUtil', None)
        self.WafLimit = kwargs.get('WafLimit', None)
        self.WafUtil = kwargs.get('WafUtil', None)
        self.AuthLimit = kwargs.get('AuthLimit', None)
        self.AuthUtil = kwargs.get('AuthUtil', None)
        self.FastviewLimit = kwargs.get('FastviewLimit', None)
        self.FastviewUtil = kwargs.get('FastviewUtil', None)

    def get_indexes(self):
        return self.vADCIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'vADCIndex',

