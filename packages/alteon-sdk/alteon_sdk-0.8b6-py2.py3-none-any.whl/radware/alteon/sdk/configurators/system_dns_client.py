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
from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from typing import ClassVar, Optional


class SystemDNSClientParameters(RadwareParametersStruct):
    primary_dns_ip4: Optional[str]
    secondary_dns_ip4: Optional[str]
    primary_dns_ip6: Optional[str]
    secondary_dns_ip6: Optional[str]
    default_domain_name: Optional[str]

    def __init__(self):
        self.primary_dns_ip4 = None
        self.secondary_dns_ip4 = None
        self.primary_dns_ip6 = None
        self.secondary_dns_ip6 = None
        self.default_domain_name = None


bean_map = {
    Root: dict(
        struct=SystemDNSClientParameters,
        direct=True,
        attrs=dict(
            dnsNewCfgPrimaryIpAddr='primary_dns_ip4',
            dnsNewCfgSecondaryIpAddr='secondary_dns_ip4',
            dnsNewCfgPrimaryIpv6Addr='primary_dns_ip6',
            dnsNewCfgSecondaryIpv6Addr='secondary_dns_ip6',
            dnsNewCfgDomainName='default_domain_name',
        )
    )
}


class SystemDNSClientConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemDNSClientParameters]

    def __init__(self, alteon_connection):
        super(SystemDNSClientConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SystemDNSClientParameters) -> SystemDNSClientParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SystemDNSClientParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SystemDNSClientParameters, dry_run=False, **kw) -> str:
        dns_params = SystemDNSClientParameters()
        dns_params.default_domain_name = ''
        dns_params.primary_dns_ip4 = '0.0.0.0'
        dns_params.secondary_dns_ip4 = '0.0.0.0'
        dns_params.primary_dns_ip6 = '0:0:0:0:0:0:0:0'
        dns_params.secondary_dns_ip6 = '0:0:0:0:0:0:0:0'
        self._write_device_beans(dns_params, dry_run=dry_run)
        return 'DNS Configuration' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            default_domain_name='',
            primary_dns_ip4='0.0.0.0',
            secondary_dns_ip4='0.0.0.0',
            primary_dns_ip6='0:0:0:0:0:0:0:0',
            secondary_dns_ip6='0:0:0:0:0:0:0:0'
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure


