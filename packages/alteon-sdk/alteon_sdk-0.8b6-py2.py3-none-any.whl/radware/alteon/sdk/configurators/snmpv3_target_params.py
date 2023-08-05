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
from radware.alteon.beans.SnmpTargetParamsTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SNMPv3TargetParamsParameters(RadwareParametersStruct):
    name: str
    usm_user_name: Optional[str]
    message_procces_model: Optional[EnumMsgProcModel]
    security_model: Optional[EnumSecurityModel]
    security_level: Optional[EnumSecurityLevel]

    def __init__(self, Name: int = None):
        self.name = Name
        self.usm_user_name = None
        self.message_procces_model = None
        self.security_model = None
        self.security_level = None

bean_map = {
    SnmpTargetParamsTable: dict(
        struct=SNMPv3TargetParamsParameters,
        direct=True,
        attrs=dict(
            Name='name',
            SecurityName='usm_user_name',
            MPModel='message_procces_model',
            SecurityModel='security_model',
            SecurityLevel='security_level'
        )
    )
}


class SNMPv3TargetParamsConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3TargetParamsParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3TargetParamsConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3TargetParamsParameters) -> SNMPv3TargetParamsParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3TargetParamsParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SnmpTargetParamsTable, parameters)

