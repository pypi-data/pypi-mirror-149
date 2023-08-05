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


from radware.sdk.configurator import DryRunDeleteProcedure
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from typing import List, Optional, ClassVar
from radware.sdk.exceptions import DeviceConfiguratorError


class AlteonCliCommandParameters(RadwareParametersStruct):
    alteon_cli_command: Optional[str]


    def __init__(self):
        self.alteon_cli_command = None


bean_map = {
    Root: dict(
        struct=AlteonCliCommandParameters,
        direct=True,
        attrs=dict(
            agAlteonCliCommand='alteon_cli_command'
        )
    )
}


class AlteonCliCommandConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[AlteonCliCommandParameters]

    def __init__(self, alteon_connection):
        super(AlteonCliCommandConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: AlteonCliCommandParameters) -> AlteonCliCommandParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: AlteonCliCommandParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

