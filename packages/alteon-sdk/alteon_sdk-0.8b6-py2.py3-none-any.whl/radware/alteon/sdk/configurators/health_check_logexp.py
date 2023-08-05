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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.SlbNewAdvhcLogexpTable import *
from radware.sdk.beans_common import *
from typing import Optional, ClassVar


class EnumSlbAdvhcTcpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HealthCheckLogExpParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    logical_expression: Optional[str]
    standalone_real_hc_mode: Optional[EnumSlbAdvhcTcpState]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.logical_expression = None
        self.standalone_real_hc_mode = None


bean_map = {
    SlbNewAdvhcLogexpTable: dict(
        struct=HealthCheckLogExpParameters,
        direct=True,
        attrs=dict(
            ID='index',
            Name='description',
            Text='logical_expression',
            Always='standalone_real_hc_mode'
        )
    )
}


class HealthCheckLogExpConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[HealthCheckLogExpParameters]

    def __init__(self, alteon_connection):
        super(HealthCheckLogExpConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: HealthCheckLogExpParameters) -> HealthCheckLogExpParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.standalone_real_hc_mode = EnumSlbAdvhcTcpState.enum(parameters.standalone_real_hc_mode)
            return parameters

    def _update(self, parameters: HealthCheckLogExpParameters, dry_run: bool) -> str:
        parameters.standalone_real_hc_mode = self._enum_to_int(EnumSlbAdvhcTcpState, parameters.standalone_real_hc_mode)
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewAdvhcLogexpTable, parameters)

    ##override
    def delete(self, parameters: HealthCheckLogExpParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        if self.read(parameters):
            self_obj = self._entry_bean_instance(parameters)
            self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

