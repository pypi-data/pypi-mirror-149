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


from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewCfgAppShapeTable import *
from typing import Optional, ClassVar


class AppshapeParameters(RadwareParametersStruct):
    index: str
    state: Optional[EnumSlbAppShapeState]
    content: Optional[str]

    def __init__(self, index: str = None):
        self.index = index
        self.state = None
        self.content = None


bean_map = {
    SlbNewCfgAppShapeTable: dict(
        struct=AppshapeParameters,
        direct=True,
        attrs=dict(
            Index='index',
            State='state'
        )
    )
}


class AppshapeConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[AppshapeParameters]

    def __init__(self, alteon_connection):
        super(AppshapeConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: AppshapeParameters) -> AppshapeParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.content = self._rest.read_data_object('getappshape?id=' + self._get_object_id(parameters))
            return parameters

    def _update(self, parameters: AppshapeParameters, dry_run: bool) -> str:
        if parameters.content:
            self._rest.update_data_object('appshapeimport?id=' + self._get_object_id(parameters), parameters.content,
                                          dry_run=dry_run)
        self._write_device_beans(parameters, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgAppShapeTable, parameters)

