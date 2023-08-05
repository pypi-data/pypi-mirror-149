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
from radware.alteon.beans.IpNewCfgStaticRouteTable import *
from radware.alteon.beans.Ipv6NewCfgStaticRouteTable import *
from typing import List, Optional, ClassVar


class IPv4RouteEntry(RadwareParametersStruct):
    network: str
    subnet: str
    gateway: str
    interface: Optional[int]

    def __init__(self, network: str = None, subnet: str = None, gateway: str = None):
        self.network = network
        self.subnet = subnet
        self.gateway = gateway
        self.interface = None


class IPv6RouteEntry(RadwareParametersStruct):
    network: str
    prefix: int
    gateway: str
    vlan: Optional[int]

    def __init__(self, network: str = None, prefix: int = None, gateway: str = None):
        self.network = network
        self.prefix = prefix
        self.gateway = gateway
        self.vlan = None


class StaticRoutesParameters(RadwareParametersStruct):
    ip4_routes: Optional[List[IPv4RouteEntry]]
    ip6_routes: Optional[List[IPv6RouteEntry]]

    def __init__(self):
        self.ip4_routes = list()
        self.ip6_routes = list()


bean_map = {
    IpNewCfgStaticRouteTable: dict(
        struct=List[IPv4RouteEntry],
        direct=True,
        attrs=dict(
            DestIp='network',
            Mask='subnet',
            Gateway='gateway',
            Interface='interface'
        )
    ),
    Ipv6NewCfgStaticRouteTable: dict(
        struct=List[IPv6RouteEntry],
        direct=True,
        attrs=dict(
            DestIp='network',
            Mask='prefix',
            Gateway='gateway',
            Vlan='vlan'
        )
    )
}


class StaticRoutesConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[StaticRoutesParameters]

    def __init__(self, alteon_connection):
        super(StaticRoutesConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: StaticRoutesParameters) -> StaticRoutesParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: StaticRoutesParameters, dry_run: bool) -> str:
        self._assign_write_numeric_index_beans(IpNewCfgStaticRouteTable, parameters.ip4_routes, dry_run=dry_run)
        self._assign_write_numeric_index_beans(Ipv6NewCfgStaticRouteTable, parameters.ip6_routes, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: StaticRoutesParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))

        def _delete_route(bean_class):
            route_entries = self._device_api.read_all(bean_class())
            for route_entry in route_entries:
                self._device_api.delete(route_entry, dry_run=dry_run)

        _delete_route(IpNewCfgStaticRouteTable)
        _delete_route(Ipv6NewCfgStaticRouteTable)
        return 'static routes' + MSG_DELETE

    def _update_remove(self, parameters: StaticRoutesParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.ip4_routes, dry_run=dry_run)
        self._remove_device_beans_by_struct_collection(parameters.ip6_routes, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(None, parameters)

