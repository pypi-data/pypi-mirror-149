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
from radware.alteon.beans.HaFloatIpNewCfgTable import *
from typing import Optional, ClassVar


class FloatingIPParameters(RadwareParametersStruct):
    index: str
    state: Optional[EnumHaFloatIpState]
    ip_ver: Optional[EnumHaFloatIpIpVer]
    ip4_address: Optional[str]
    ip6_address: Optional[str]
    interface: Optional[int]

    def __init__(self, index: str = None):
        self.index = index
        self.state = None
        self.ip_ver = None
        self.ip4_address = None
        self.ip6_address = None
        self.interface = None


bean_map = {
    HaFloatIpNewCfgTable: dict(
        struct=FloatingIPParameters,
        direct=True,
        attrs=dict(
            Index='index',
            State='state',
            IpVer='ip_ver',
            IpAddr='ip4_address',
            Ipv6Addr='ip6_address',
            If='interface'
        )
    )
}


class FloatingIPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[FloatingIPParameters]

    def __init__(self, alteon_connection):
        super(FloatingIPConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: FloatingIPParameters) -> FloatingIPParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: FloatingIPParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(HaFloatIpNewCfgTable, parameters)

