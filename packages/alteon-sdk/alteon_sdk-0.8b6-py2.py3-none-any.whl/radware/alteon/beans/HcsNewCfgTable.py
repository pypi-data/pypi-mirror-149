
from radware.sdk.beans_common import *


class EnumHcsAddCloseCmd(BaseBeanEnum):
    other = 1
    close = 2


class EnumHcsRemLastCmd(BaseBeanEnum):
    other = 1
    remove = 2


class EnumHcsDeleteScript(BaseBeanEnum):
    other = 1
    delete = 2


class HcsNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ScriptIndex = kwargs.get('ScriptIndex', None)
        self.ScriptString = kwargs.get('ScriptString', None)
        self.AddCloseCmd = EnumHcsAddCloseCmd.enum(kwargs.get('AddCloseCmd', None))
        self.RemLastCmd = EnumHcsRemLastCmd.enum(kwargs.get('RemLastCmd', None))
        self.DeleteScript = EnumHcsDeleteScript.enum(kwargs.get('DeleteScript', None))
        self.AddOffsetCmd = kwargs.get('AddOffsetCmd', None)
        self.AddWaitCmd = kwargs.get('AddWaitCmd', None)
        self.AddOpenProtCmd = kwargs.get('AddOpenProtCmd', None)
        self.AddDepthCmd = kwargs.get('AddDepthCmd', None)
        self.AddLongBsendCmd = kwargs.get('AddLongBsendCmd', None)
        self.AddLongBexpectCmd = kwargs.get('AddLongBexpectCmd', None)
        self.AddLongSendCmd = kwargs.get('AddLongSendCmd', None)
        self.AddLongExpectCmd = kwargs.get('AddLongExpectCmd', None)
        self.AddLongNsendCmd = kwargs.get('AddLongNsendCmd', None)
        self.AddLongNexpectCmd = kwargs.get('AddLongNexpectCmd', None)

    def get_indexes(self):
        return self.ScriptIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ScriptIndex',

