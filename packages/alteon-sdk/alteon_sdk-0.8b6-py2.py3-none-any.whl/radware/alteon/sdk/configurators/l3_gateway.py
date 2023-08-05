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
from radware.alteon.beans.IpNewCfgGwTable import *
from radware.alteon.beans.Global import EnumIpNewCfgGwMetric, Root
from radware.alteon.beans.GatewayInfoTable import GatewayInfoTable
from typing import Optional, ClassVar, Dict


class EnumGatewayHC(BaseBeanEnum):
    arp = 2
    icmp = 3


class GatewayParameters(RadwareParametersStruct):
    index: int
    state: Optional[EnumIpGwState]
    ip_ver: Optional[EnumIpGwIpVer]
    ip4_address: Optional[str]
    ip6_address: Optional[str]
    vlan: Optional[int]
    health_check_type: Optional[EnumGatewayHC]
    health_check_interval_second: Optional[int]
    health_check_retries: Optional[int]
    route_priority: Optional[EnumIpGwPriority]
    global_gateway_metric: Optional[EnumIpNewCfgGwMetric]

    def __init__(self, index: int = None):
        self.index = index
        self.state = None
        self.ip_ver = None
        self.ip4_address = None
        self.ip6_address = None
        self.vlan = None
        self.health_check_type = None
        self.health_check_interval_second = None
        self.health_check_retries = None
        self.route_priority = None
        self.global_gateway_metric = None


bean_map = {
    IpNewCfgGwTable: dict(
        struct=GatewayParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Addr='ip4_address',
            Interval='health_check_interval_second',
            Retry='health_check_retries',
            State='state',
            Vlan='vlan',
            IpVer='ip_ver',
            Ipv6Addr='ip6_address',
            Priority='route_priority',
        )
    )
}

bean_state_map = {
    GatewayInfoTable: dict()
}


class GatewayConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[GatewayParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(GatewayConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: GatewayParameters) -> GatewayParameters:
        self._read_device_beans(parameters)
        if self._beans:
            if self._beans[IpNewCfgGwTable].Arp == EnumIpGwArp.enabled:
                parameters.health_check_type = EnumGatewayHC.arp
            else:
                parameters.health_check_type = EnumGatewayHC.icmp

            root = Root()
            root.ipNewCfgGwMetric = READ_PROP
            parameters.global_gateway_metric = self._device_api.read(root).ipNewCfgGwMetric
            return parameters

    def _update(self, parameters: GatewayParameters, dry_run: bool) -> str:

        if parameters.health_check_type:
            bean = self._entry_bean_instance(parameters)
            if EnumGatewayHC.arp == parameters.health_check_type:
                bean.Arp = EnumIpGwArp.enabled
            else:
                bean.Arp = EnumIpGwArp.disabled
            self._device_api.update(bean, dry_run=dry_run)

        if parameters.global_gateway_metric is not None:
            root = Root()
            root.ipNewCfgGwMetric = parameters.global_gateway_metric
            self._device_api.update(root, dry_run=dry_run)

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(IpNewCfgGwTable, parameters)
