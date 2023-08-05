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
from radware.alteon.beans.SlbNewAdvhcTcpTable import *
from radware.sdk.beans_common import *
from typing import Optional, ClassVar


class EnumSlbAdvhcTcpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAdvhcTcpIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2
    none = 3


class HealthCheckTCPParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    destination_port: Optional[int]
    ip_ver: Optional[EnumSlbAdvhcTcpIpVer]
    destination_ip_or_hostname: Optional[str]
    transparent_health_check: Optional[EnumSlbAdvhcTcpState]
    interval_second: Optional[int]
    retries_failure: Optional[int]
    retries_restore: Optional[int]
    response_timeout_second: Optional[int]
    interval_downtime_second: Optional[int]
    invert_result: Optional[EnumSlbAdvhcTcpState]
    connection_termination: Optional[EnumSlbAdvhcTcpConnTerm]
    standalone_real_hc_mode: Optional[EnumSlbAdvhcTcpState]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.destination_port = None
        self.ip_ver = None
        self.destination_ip_or_hostname = None
        self.transparent_health_check = None
        self.interval_second = None
        self.retries_failure = None
        self.retries_restore = None
        self.response_timeout_second = None
        self.interval_downtime_second = None
        self.invert_result = None
        self.connection_termination = None
        self.standalone_real_hc_mode = None


bean_map = {
    SlbNewAdvhcTcpTable: dict(
        struct=HealthCheckTCPParameters,
        direct=True,
        attrs=dict(
            ID='index',
            Name='description',
            DPort='destination_port',
            IPVer='ip_ver',
            HostName='destination_ip_or_hostname',
            Transparent='transparent_health_check',
            Interval='interval_second',
            Retries='retries_failure',
            RestoreRetries='retries_restore',
            Timeout='response_timeout_second',
            DownInterval='interval_downtime_second',
            Invert='invert_result',
            ConnTerm='connection_termination',
            Always='standalone_real_hc_mode'
        )
    )
}


class HealthCheckTCPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[HealthCheckTCPParameters]

    def __init__(self, alteon_connection):
        super(HealthCheckTCPConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: HealthCheckTCPParameters) -> HealthCheckTCPParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.ip_ver = EnumSlbAdvhcTcpIpVer.enum(parameters.ip_ver)
            parameters.invert_result = EnumSlbAdvhcTcpState.enum(parameters.invert_result)
            parameters.transparent_health_check = EnumSlbAdvhcTcpState.enum(parameters.transparent_health_check)
            parameters.standalone_real_hc_mode = EnumSlbAdvhcTcpState.enum(parameters.standalone_real_hc_mode)
            return parameters

    def _update(self, parameters: HealthCheckTCPParameters, dry_run: bool) -> str:
        parameters.ip_ver = self._enum_to_int(EnumSlbAdvhcTcpIpVer, parameters.ip_ver)
        parameters.invert_result = self._enum_to_int(EnumSlbAdvhcTcpState, parameters.invert_result)
        parameters.transparent_health_check = self._enum_to_int(EnumSlbAdvhcTcpState,
                                                                parameters.transparent_health_check)
        parameters.standalone_real_hc_mode = self._enum_to_int(EnumSlbAdvhcTcpState, parameters.standalone_real_hc_mode)

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewAdvhcTcpTable, parameters)

    ##override
    def delete(self, parameters: HealthCheckTCPParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        if self.read(parameters):
            self_obj = self._entry_bean_instance(parameters)
            self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

