
from radware.sdk.beans_common import *


class EnumLayer7ContentClassHostName(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassPath(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassFileName(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassFileType(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassHeader(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassCookie(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassText(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassXMLTag(BaseBeanEnum):
    yes = 1
    no = 2


class EnumLayer7ContentClassDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumLayer7ContentClassType(BaseBeanEnum):
    http = 1
    rtsp = 3
    ssl = 6


class Layer7NewCfgContentClassTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.LogicalExpression = kwargs.get('LogicalExpression', None)
        self.HostName = EnumLayer7ContentClassHostName.enum(kwargs.get('HostName', None))
        self.Path = EnumLayer7ContentClassPath.enum(kwargs.get('Path', None))
        self.FileName = EnumLayer7ContentClassFileName.enum(kwargs.get('FileName', None))
        self.FileType = EnumLayer7ContentClassFileType.enum(kwargs.get('FileType', None))
        self.Header = EnumLayer7ContentClassHeader.enum(kwargs.get('Header', None))
        self.Cookie = EnumLayer7ContentClassCookie.enum(kwargs.get('Cookie', None))
        self.Text = EnumLayer7ContentClassText.enum(kwargs.get('Text', None))
        self.XMLTag = EnumLayer7ContentClassXMLTag.enum(kwargs.get('XMLTag', None))
        self.Delete = EnumLayer7ContentClassDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)
        self.Type = EnumLayer7ContentClassType.enum(kwargs.get('Type', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

