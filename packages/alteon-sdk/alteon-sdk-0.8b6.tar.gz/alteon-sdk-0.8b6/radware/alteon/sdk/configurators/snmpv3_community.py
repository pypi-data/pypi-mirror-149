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
from radware.alteon.beans.SnmpCommunityTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError


class SNMPv3CommunityParameters(RadwareParametersStruct):
    index: str
    community_name: Optional[str]
    security_name: Optional[str]
    transport_tag: Optional[str]


    def __init__(self, index: str = None):
        self.index = index
        self.community_name = None
        self.security_name = None
        self.transport_tag = None

bean_map = {
    SnmpCommunityTable: dict(
        struct=SNMPv3CommunityParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Name='community_name',
            SecurityName='security_name',
            TransportTag='transport_tag',
        )
    )
}


class SNMPv3CommunityConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3CommunityParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3CommunityConfigurator, self).__init__(bean_map, alteon_connection)        

    def _read(self, parameters: SNMPv3CommunityParameters) -> SNMPv3CommunityParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3CommunityParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SnmpCommunityTable, parameters)


