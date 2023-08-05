#!/usr/bin/env python
# Copyright (c) 2019 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewCfgEnhGroupRealServerTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError


class GroupRealServerParameters(RadwareParametersStruct):
    group_index: str
    real_server_index: str
    real_server_status: Optional[EnumSlbGroupRealServerState]


    def __init__(self, index: str = None, real_index: str = None):
        self.group_index = index
        self.real_server_index = real_index
        self.real_server_status = None

bean_map = {
    SlbNewCfgEnhGroupRealServerTable: dict(
        struct=GroupRealServerParameters,
        direct=True,
        attrs=dict(
            RealServGroupIndex='group_index',
            ServIndex='real_server_index',
            State='real_server_status'
        )
    )
}


class GroupRealServerConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[GroupRealServerParameters]

    def __init__(self, alteon_connection):
        super(GroupRealServerConfigurator, self).__init__(bean_map, alteon_connection)        
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: GroupRealServerParameters) -> GroupRealServerParameters:
        log.debug('group_real_server_read {0}'.format(parameters))
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: GroupRealServerParameters, dry_run: bool) -> str:
        log.debug('group_real_server_update {0}'.format(parameters))
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgEnhGroupRealServerTable, parameters)


