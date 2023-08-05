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
from radware.alteon.beans.VacmSecurityToGroupTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SNMPv3GroupParameters(RadwareParametersStruct):
    security_model: EnumSecurityModel
    usm_user_name: str
    group_name: Optional[str]

    def __init__(self, secModel: EnumSecurityModel = None, Name: str = None):
        self.security_model = secModel
        self.usm_user_name = Name
        self.group_name = None

bean_map = {
    VacmSecurityToGroupTable: dict(
        struct=SNMPv3GroupParameters,
        direct=True,
        attrs=dict(
            Model='security_model',
            Name='usm_user_name',
            GroupName='group_name'
        )
    )
}


class SNMPv3GroupConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3GroupParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3GroupConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3GroupParameters) -> SNMPv3GroupParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3GroupParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(VacmSecurityToGroupTable, parameters)

#    def delete(self, parameters: SNMPv3UsmUserParameters, dry_run=False, **kw) -> str:
#        if self.read(parameters):
#            self_obj = self._entry_bean_instance(parameters)
#            self_obj.EngineID = 1
#            self._device_api.delete(self_obj, dry_run=dry_run)
#        return self._get_object_id(parameters) + MSG_DELETE

