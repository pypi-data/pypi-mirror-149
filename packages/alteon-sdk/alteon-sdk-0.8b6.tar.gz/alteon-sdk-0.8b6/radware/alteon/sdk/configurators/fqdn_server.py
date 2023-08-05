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
from radware.alteon.beans.SlbNewCfgFQDNServerTable import *
from typing import Optional, ClassVar


class FQDNServerParameters(RadwareParametersStruct):
    index: str
    fqdn: Optional[str]
    ip_ver: Optional[EnumSlbFQDNServerIpVers]
    ttl: Optional[int]
    group_id: Optional[str]
    template_server_name: Optional[str]
    state: Optional[EnumSlbFQDNServerState]

    def __init__(self, index: str = None):
        self.index = index
        self.fqdn = None
        self.ip_ver = None
        self.ttl = None
        self.group_id = None
        self.template_server_name = None
        self.state = None


bean_map = {
    SlbNewCfgFQDNServerTable: dict(
        struct=FQDNServerParameters,
        direct=True,
        attrs=dict(
            IdIndex='index',
            FQDN='fqdn',
            IpVers='ip_ver',
            TTL='ttl',
            Group='group_id',
            Templ='template_server_name',
            State='state'
        )
    )
}


class FQDNServerConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[FQDNServerParameters]

    def __init__(self, alteon_connection):
        super(FQDNServerConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: FQDNServerParameters) -> FQDNServerParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: FQDNServerParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgFQDNServerTable, parameters)


