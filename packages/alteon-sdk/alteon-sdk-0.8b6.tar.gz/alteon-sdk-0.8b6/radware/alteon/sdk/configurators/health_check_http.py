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
from radware.alteon.beans.SlbNewAdvhcHttpTable import *
from radware.sdk.beans_common import *
from typing import Optional, ClassVar


class EnumSlbAdvhcHttpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAdvhcHttpIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2
    none = 3


class HealthCheckHTTPParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    destination_port: Optional[int]
    ip_ver: Optional[EnumSlbAdvhcHttpIpVer]
    destination_ip_or_hostname: Optional[str]
    transparent_health_check: Optional[EnumSlbAdvhcHttpState]
    interval_second: Optional[int]
    retries_failure: Optional[int]
    retries_restore: Optional[int]
    response_timeout_second: Optional[int]
    interval_downtime_second: Optional[int]
    invert_result: Optional[EnumSlbAdvhcHttpState]
    connection_termination: Optional[EnumSlbAdvhcHttpConnTerm]
    standalone_real_hc_mode: Optional[EnumSlbAdvhcHttpState]
    https: Optional[EnumSlbAdvhcHttpState]
    http_hostname: Optional[str]
    http_path: Optional[str]
    http_method: Optional[EnumSlbAdvhcHttpMethod]
    http_headers_raw: Optional[str]
    http_body: Optional[str]
    authentication: Optional[EnumSlbAdvhcHttpAuthLevel]
    auth_username: Optional[str]
    auth_password: Optional[PasswordArgument]
    return_string_lookup_type: Optional[EnumSlbAdvhcHttpResponseType]
    overload_string_lookup_type: Optional[EnumSlbAdvhcHttpOverloadType]
    expected_return_codes: Optional[str]
    return_value: Optional[str]
    overload_value: Optional[str]
    proxy_request: Optional[EnumSlbAdvhcHttpState]
    https_cipher: Optional[EnumSlbAdvhcHttpHttpsCipherName]
    https_user_defined_cipher: Optional[str]
    http2: Optional[EnumSlbAdvhcHttpState]

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
        self.https = None
        self.http_hostname = None
        self.http_path = None
        self.http_method = None
        self.http_headers_raw = None
        self.http_body = None
        self.authentication = None
        self.auth_username = None
        self.auth_password = None
        self.return_string_lookup_type = None
        self.overload_string_lookup_type = None
        self.expected_return_codes = None
        self.return_value = None
        self.overload_value = None
        self.proxy_request = None
        self.https_cipher = None
        self.https_user_defined_cipher = None
        self.http2 = None


bean_map = {
    SlbNewAdvhcHttpTable: dict(
        struct=HealthCheckHTTPParameters,
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
            Always='standalone_real_hc_mode',
            Https='https',
            Host='http_hostname',
            Path='http_path',
            Method='http_method',
            Headers='http_headers_raw',
            Body='http_body',
            AuthLevel='authentication',
            UserName='auth_username',
            Password='auth_password',
            ResponseType='return_string_lookup_type',
            OverloadType='overload_string_lookup_type',
            ResponseCode='expected_return_codes',
            ReceiveString='return_value',
            OverloadString='overload_value',
            Proxy='proxy_request',
            HttpsCipherName='https_cipher',
            HttpsCipherUserdef='https_user_defined_cipher',
            Http2='http2'
        )
    )
}


class HealthCheckHTTPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[HealthCheckHTTPParameters]

    def __init__(self, alteon_connection):
        super(HealthCheckHTTPConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: HealthCheckHTTPParameters) -> HealthCheckHTTPParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.ip_ver = EnumSlbAdvhcHttpIpVer.enum(parameters.ip_ver)
            parameters.invert_result = EnumSlbAdvhcHttpState.enum(parameters.invert_result)
            parameters.transparent_health_check = EnumSlbAdvhcHttpState.enum(parameters.transparent_health_check)
            parameters.standalone_real_hc_mode = EnumSlbAdvhcHttpState.enum(parameters.standalone_real_hc_mode)
            parameters.https = EnumSlbAdvhcHttpState.enum(parameters.https)
            parameters.http2 = EnumSlbAdvhcHttpState.enum(parameters.http2)
            parameters.proxy_request = EnumSlbAdvhcHttpState.enum(parameters.proxy_request)
            return parameters

    def _update(self, parameters: HealthCheckHTTPParameters, dry_run: bool) -> str:
        parameters.ip_ver = self._enum_to_int(EnumSlbAdvhcHttpIpVer, parameters.ip_ver)
        parameters.invert_result = self._enum_to_int(EnumSlbAdvhcHttpState, parameters.invert_result)
        parameters.transparent_health_check = self._enum_to_int(EnumSlbAdvhcHttpState,
                                                                parameters.transparent_health_check)
        parameters.standalone_real_hc_mode = self._enum_to_int(EnumSlbAdvhcHttpState, parameters.standalone_real_hc_mode)
        parameters.https = self._enum_to_int(EnumSlbAdvhcHttpState, parameters.https)
        parameters.http2 = self._enum_to_int(EnumSlbAdvhcHttpState, parameters.http2)
        parameters.proxy_request = self._enum_to_int(EnumSlbAdvhcHttpState, parameters.proxy_request)
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewAdvhcHttpTable, parameters)

    ##override
    def delete(self, parameters: HealthCheckHTTPParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        if self.read(parameters):
            self_obj = self._entry_bean_instance(parameters)
            self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE



