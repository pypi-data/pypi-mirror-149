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
from radware.alteon.beans.IpNewCfgIntfTable import *
from radware.alteon.beans.IpIntfInfoTable import IpIntfInfoTable
from typing import Optional, ClassVar, Dict


class L3InterfaceParameters(RadwareParametersStruct):
    index: int
    description: Optional[str]
    ip4_address: Optional[str]
    ip4_subnet: Optional[str]
    vlan: Optional[int]
    state: Optional[EnumIpIntfState]
    bootp_relay: Optional[EnumIpIntfBootpRelay]
    ip_ver: Optional[EnumIpIntfIpVer]
    ip6_address: Optional[str]
    ip6_prefix: Optional[int]
    peer_ip: Optional[str]

    def __init__(self, index: int = None):
        self.index = index
        self.description = None
        self.ip4_address = None
        self.ip4_subnet = None
        self.vlan = None
        self.state = None
        self.bootp_relay = None
        self.ip_ver = None
        self.ip6_address = None
        self.ip6_prefix = None
        self.peer_ip = None


bean_map = {
    IpNewCfgIntfTable: dict(
        struct=L3InterfaceParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Addr='ip4_address',
            Mask='ip4_subnet',
            Vlan='vlan',
            State='state',
            BootpRelay='bootp_relay',
            IpVer='ip_ver',
            Ipv6Addr='ip6_address',
            PrefixLen='ip6_prefix',
            Peer='peer_ip',
            Description='description'
        )
    )
}

bean_state_map = {
    IpIntfInfoTable: dict()
}


class L3InterfaceConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[L3InterfaceParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(L3InterfaceConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: L3InterfaceParameters) -> L3InterfaceParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: L3InterfaceParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(IpNewCfgIntfTable, parameters)

