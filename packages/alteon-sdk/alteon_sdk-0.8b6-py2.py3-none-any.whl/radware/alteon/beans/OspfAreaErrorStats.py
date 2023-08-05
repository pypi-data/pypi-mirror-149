
from radware.sdk.beans_common import *


class OspfAreaErrorStats(DeviceBean):
    def __init__(self, **kwargs):
        self.ErrIndex = kwargs.get('ErrIndex', None)
        self.ErrAuthFailure = kwargs.get('ErrAuthFailure', None)
        self.ErrNetmaskMismatch = kwargs.get('ErrNetmaskMismatch', None)
        self.ErrHelloMismatch = kwargs.get('ErrHelloMismatch', None)
        self.ErrDeadMismatch = kwargs.get('ErrDeadMismatch', None)
        self.ErrOptionsMismatch = kwargs.get('ErrOptionsMismatch', None)
        self.ErrUnknownNbr = kwargs.get('ErrUnknownNbr', None)

    def get_indexes(self):
        return self.ErrIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ErrIndex',

