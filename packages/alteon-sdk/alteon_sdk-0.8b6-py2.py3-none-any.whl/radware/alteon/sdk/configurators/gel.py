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
# @author: Ofer Epstein, Radware


from radware.sdk.configurator import DryRunDeleteProcedure
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from typing import List, Optional, ClassVar
from radware.sdk.exceptions import DeviceConfiguratorError


class GelParameters(RadwareParametersStruct):
    state: Optional[EnumGelState]
    primary_url: Optional[str]
    secondary_url: Optional[str]
    primary_dns_ipv4: Optional[str]
    secondary_dns_ipv4: Optional[str]
    primary_dns_ipv6: Optional[str]
    secondary_dns_ipv6: Optional[str]
    interval: Optional[int]
    retries: Optional[int]
    retry_interval: Optional[int]

    def __init__(self):
        self.state = None
        self.primary_url = None
        self.secondary_url = None
        self.primary_dns_ipv4 = None
        self.secondary_dns_ipv4 = None
        self.primary_dns_ipv6 = None
        self.secondary_dns_ipv6 = None
        self.interval = None
        self.retries = None
        self.retry_interval = None

bean_map = {
    Root: dict(
        struct=GelParameters,
        direct=True,
        attrs=dict(
            newCfgLmLicEnable='state',
            newCfgLmLicPrimaryURL='primary_url',
            newCfgLmLicSecondaryURL='secondary_url',
            newCfgLmLicPrimaryIpAddr='primary_dns_ipv4',
            newCfgLmLicSecondaryIpAddr='secondary_dns_ipv4',
            newCfgLmLicPrimaryIpv6Addr='primary_dns_ipv6',
            newCfgLmLicSecondaryIpv6Addr='secondary_dns_ipv6',
            newCfgLmLicInterval='interval',
            newCfgLmLicRetries='retries',
            newCfgLmLicRetryInterval='retry_interval',
        )
    )
}


class GelConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[GelParameters]

    def __init__(self, alteon_connection):
        super(GelConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: GelParameters) -> GelParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: GelParameters, dry_run: bool) -> str:
        if parameters.interval is not None:
            if parameters.interval < 20 or parameters.interval > 86400:
                raise DeviceConfiguratorError(self.__class__, 'validation interval must be between 20 and 86400 seconds')
        if parameters.retries is not None:
            if parameters.retries < 1 or parameters.retries > 100:
                raise DeviceConfiguratorError(self.__class__, 'retries must be between 1 and 100')
        if parameters.retry_interval is not None:
            if parameters.retry_interval < 20 or parameters.retry_interval > 3600:
                raise DeviceConfiguratorError(self.__class__, 'retransmition interval must be between 20 and 3600 seconds')
        if parameters.primary_dns_ipv4 is not None and parameters.primary_dns_ipv6 is not None:
            raise DeviceConfiguratorError(self.__class__, 'primary dns must be ipv4 or ipv6 not both')
        if parameters.secondary_dns_ipv4 is not None and parameters.secondary_dns_ipv6 is not None:
            raise DeviceConfiguratorError(self.__class__, 'secondary dns must be ipv4 or ipv6 not both')
        if parameters.primary_url is not None:
            if not parameters.primary_url.startswith('http://') and not parameters.primary_url.startswith('https://'):
            #if not parameters.primary_url.startswith('http://', 'https://'):
                raise DeviceConfiguratorError(self.__class__, 'primary url not a valid url')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

