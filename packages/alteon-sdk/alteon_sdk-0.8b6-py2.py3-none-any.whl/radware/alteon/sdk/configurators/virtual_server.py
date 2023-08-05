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
from radware.alteon.beans.SlbNewCfgEnhVirtServerTable import *
from typing import Optional, ClassVar


class VirtualServerParameters(RadwareParametersStruct):
    index: str
    ip_ver: Optional[EnumSlbVirtServerIpVer]
    ip_address: Optional[str]
    ip6_address: Optional[str]
    state: Optional[EnumSlbVirtServerState]
    domain_name: Optional[str]
    weight: Optional[int]
    availability: Optional[int]
    virtual_server_name: Optional[str]
    connection_rst_invalid_port: Optional[EnumSlbVirtServerCReset]
    src_network_class_id: Optional[str]
    availability_persist: Optional[EnumSlbVirtServerAvailPersist]
    wan_link_id: Optional[str]
    return_to_src_mac: Optional[EnumSlbVirtServerRtSrcMac]

    def __init__(self, index: str = None):
        self.index = index
        self.ip_ver = None
        self.ip_address = None
        self.ip6_address = None
        self.state = None
        self.domain_name = None
        self.weight = None
        self.availability = None
        self.virtual_server_name = None
        self.connection_rst_invalid_port = None
        self.src_network_class_id = None
        self.availability_persist = None
        self.wan_link_id = None
        self.return_to_src_mac = None


bean_map = {
    SlbNewCfgEnhVirtServerTable: dict(
        struct=VirtualServerParameters,
        direct=True,
        attrs=dict(
            VirtServerIndex='index',
            VirtServerIpVer='ip_ver',
            VirtServerIpAddress='ip_address',
            VirtServerIpv6Addr='ip6_address',
            VirtServerState='state',
            VirtServerDname='domain_name',
            VirtServerWeight='weight',
            VirtServerAvail='availability',
            VirtServerVname='virtual_server_name',
            VirtServerCReset='connection_rst_invalid_port',
            VirtServerSrcNetwork='src_network_class_id',
            VirtServerAvailPersist='availability_persist',
            VirtServerWanlink='wan_link_id',
            VirtServerRtSrcMac='return_to_src_mac'
        )
    )
}


class VirtualServerConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[VirtualServerParameters]

    def __init__(self, alteon_connection):
        super(VirtualServerConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: VirtualServerParameters) -> VirtualServerParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: VirtualServerParameters, dry_run: bool) -> str:
        parameters.clear_zero_ip_address()
        self._write_device_beans(parameters, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgEnhVirtServerTable, parameters)

    def free_service_index(self, parameters):
        return self._get_bean_free_index(self._get_bean_instance(SlbNewCfgEnhVirtServerTable, parameters),
                                        'VirtServerFreeServiceIdx')

