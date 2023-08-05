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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.UsmUserTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SNMPv3UsmUserParameters(RadwareParametersStruct):
    engine_id: Optional[str]
    usm_user_name: str
    authentication_protocol: Optional[EnumAuthProtocol]
    authentication_password: Optional[str]
    privacy_protocol: Optional[EnumPrivProtocol]
    privacy_password: Optional[str]

    def __init__(self, idx: str = None, Name: str = None):
        self.engine_id = idx
        self.usm_user_name = Name
        self.authentication_protocol = None
        self.authentication_password = None
        self.privacy_protocol = None
        self.privacy_password = None

bean_map = {
    UsmUserTable: dict(
        struct=SNMPv3UsmUserParameters,
        direct=True,
        attrs=dict(
            EngineID='engine_id',
            Name='usm_user_name',
            AuthProtocol='authentication_protocol',
            AuthKeyChange='authentication_password',
            PrivProtocol='privacy_protocol',
            PrivKeyChange='privacy_password'
        )
    )
}


class SNMPv3UsmUserConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3UsmUserParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3UsmUserConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3UsmUserParameters) -> SNMPv3UsmUserParameters:
        parameters.engine_id = 1
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3UsmUserParameters, dry_run: bool) -> str:
        parameters.engine_id = 1
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(UsmUserTable, parameters)

    def delete(self, parameters: SNMPv3UsmUserParameters, dry_run=False, **kw) -> str:
        if self.read(parameters):
            self_obj = self._entry_bean_instance(parameters)
            self_obj.EngineID = 1
            self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

