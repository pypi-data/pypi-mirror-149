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
from radware.alteon.beans.SnmpNotifyTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SNMPv3NotifyParameters(RadwareParametersStruct):
    name: str
    tag: Optional[str]
    
    def __init__(self, name: str = None):
        self.name = name
        self.tag = None

bean_map = {
    SnmpNotifyTable: dict(
        struct=SNMPv3NotifyParameters,
        direct=True,
        attrs=dict(
            Name='name',
            Tag='tag',
        )
    )
}


class SNMPv3NotifyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3NotifyParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3NotifyConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3NotifyParameters) -> SNMPv3NotifyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3NotifyParameters, dry_run: bool) -> str:
        if parameters.name is not None:
            if len(parameters.name) > 32:
                raise DeviceConfiguratorError(self.__class__, 'max Notify name length must be between 1 and 32')
        if parameters.tag is not None:
            if len(parameters.tag) > 255:
                raise DeviceConfiguratorError(self.__class__, 'max Notify tag length must be between 1 and 255')

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SnmpNotifyTable, parameters)

