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
from radware.alteon.beans.SlbNewCfgEnhRealServerTable import *
from radware.alteon.beans.SlbNewCfgEnhRealServerSecondPartTable import *
from radware.alteon.beans.SlbNewCfgEnhRealServerThirdPartTable import *
from radware.alteon.beans.SlbNewCfgEnhRealServPortTable import *
from radware.alteon.beans.SlbEnhRealServerInfoTable import SlbEnhRealServerInfoTable
from typing import List, Optional, ClassVar, Dict


class ServerParameters(RadwareParametersStruct):
    index: str
    state: Optional[EnumSlbRealServerState]
    ip_ver: Optional[EnumSlbRealServerIpVer]
    ip_address: Optional[str]
    ip6_address: Optional[str]
    weight: Optional[int]
    max_connections: Optional[int]
    connection_mode: Optional[EnumSlbRealServerMode]
    availability: Optional[int]
    server_type: Optional[EnumSlbRealServerType]
    nat_mode: Optional[EnumSlbRealServerProxyIpMode]
    nat_address: Optional[str]
    nat_subnet: Optional[str]
    nat6_address: Optional[str]
    nat6_prefix: Optional[int]
    nat_ip_persistency: Optional[EnumSlbRealServerProxyIpPersistency]
    nat_network_class_name: Optional[str]
    nat_net_class_ip_persistency: Optional[EnumSlbRealServerProxyIpNWclassPersistency]
    health_check_id: Optional[str]
    server_ports: Optional[List[int]]
    name: Optional[str]

    def __init__(self, index: str = None):
        self.index = index
        self.state = None
        self.ip_ver = None
        self.ip_address = None
        self.ip6_address = None
        self.weight = None
        self.max_connections = None
        self.connection_mode = None
        self.availability = None
        self.server_type = None
        self.nat_mode = None
        self.nat_address = None
        self.nat_subnet = None
        self.nat6_address = None
        self.nat6_prefix = None
        self.nat_ip_persistency = None
        self.nat_network_class_name = None
        self.nat_net_class_ip_persistency = None
        self.health_check_id = None
        self.server_ports = list()
        self.name = None


bean_map = {
    SlbNewCfgEnhRealServerTable: dict(
        struct=ServerParameters,
        direct=True,
        attrs=dict(
            Index='index',
            State='state',
            IpVer='ip_ver',
            IpAddr='ip_address',
            Ipv6Addr='ip6_address',
            Weight='weight',
            Type='server_type',
            MaxConns='max_connections',
            Name="name"
        )
    ),
    SlbNewCfgEnhRealServerSecondPartTable: dict(
        struct=ServerParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Avail='availability',
            Mode='connection_mode',
            ProxyIpMode='nat_mode',
            ProxyIpAddr='nat_address',
            ProxyIpMask='nat_subnet',
            ProxyIpv6Addr='nat6_address',
            ProxyIpv6Prefix='nat6_prefix',
            ProxyIpPersistency='nat_ip_persistency',
            ProxyIpNWclass='nat_network_class_name',
            ProxyIpNWclassPersistency='nat_net_class_ip_persistency',
        )
    ),
    SlbNewCfgEnhRealServerThirdPartTable: dict(
        struct=ServerParameters,
        direct=True,
        attrs=dict(
            Index='index',
            HealthID='health_check_id'
        )
    ),
    SlbNewCfgEnhRealServPortTable: dict(
        struct=List[ServerParameters],
        direct=False,
        attrs=dict(
            Index='index'
        )
    )
}

bean_state_map = {
    SlbEnhRealServerInfoTable: dict(exclude=['UpTime', 'DownTime', 'LastFailureTime'])
}


class ServerConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[ServerParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(ServerConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: ServerParameters) -> ServerParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.server_ports = list()
            for port_entry in self._beans[SlbNewCfgEnhRealServPortTable]:
                parameters.server_ports.append(port_entry.RealPort)
            return parameters

    def _update(self, parameters: ServerParameters, dry_run: bool) -> str:
        def _get_next_rport_idx():
            res = self._get_bean_free_index(self._entry_bean_instance(parameters), 'NxtRportIdx')
            if res:
                return res
            return 1

        parameters.clear_zero_ip_address()
        self._write_device_beans(parameters, dry_run=dry_run)
        if parameters.server_ports:
            for server_port in parameters.server_ports:
                real_port = self._get_bean_instance(SlbNewCfgEnhRealServPortTable, parameters)
                real_port.RealPort = server_port
                real_port.PortIndex = _get_next_rport_idx()
                self._device_api.update(real_port, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: ServerParameters, dry_run: bool) -> str:
        instance = SlbNewCfgEnhRealServPortTable()
        instance.Index = parameters.index
        self._remove_device_beans_by_simple_collection(parameters.server_ports, instance, 'RealPort', dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgEnhRealServerTable, parameters)

