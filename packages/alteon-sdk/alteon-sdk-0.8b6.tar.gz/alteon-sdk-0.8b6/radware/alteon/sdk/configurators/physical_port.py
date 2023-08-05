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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_NO_DELETE, AlteonConfigurator
from radware.alteon.beans.IpFwdNewCfgPortTable import *
from radware.alteon.beans.AgPortNewCfgTable import *
from radware.alteon.beans.PortInfoTable import PortInfoTable
from radware.alteon.beans.PortStatsTable import *
from typing import Optional, ClassVar, Dict


class PhysicalPortParameters(RadwareParametersStruct):
    index: int
    state: Optional[EnumAgPortState]
    vlan_tag_mode: Optional[EnumAgPortVlanTag]
    rmon_state: Optional[EnumAgPortRmon]
    pvid: Optional[int]
    name: Optional[str]
    traffic_contract_id: Optional[int]
    discard_non_ip_traffic: Optional[EnumAgPortDiscardNonIPs]
    link_state_trap: Optional[EnumAgPortLinkTrap]
    port_alias: Optional[str]
    spanning_tree_state: Optional[EnumAgPortPortStp]
    ip_forwarding: Optional[EnumIpFwdPortState]

    def __init__(self, index: int = None):
        self.index = index
        self.state = None
        self.vlan_tag_mode = None
        self.rmon_state = None
        self.pvid = None
        self.name = None
        self.traffic_contract_id = None
        self.discard_non_ip_traffic = None
        self.link_state_trap = None
        self.port_alias = None
        self.spanning_tree_state = None
        self.ip_forwarding = None


bean_map = {
    AgPortNewCfgTable: dict(
        struct=PhysicalPortParameters,
        direct=True,
        attrs=dict(
            Indx='index',
            State='state',
            VlanTag='vlan_tag_mode',
            Rmon='rmon_state',
            PVID='pvid',
            PortName='name',
            BwmContract='traffic_contract_id',
            DiscardNonIPs='discard_non_ip_traffic',
            LinkTrap='link_state_trap',
            PortAlias='port_alias',
            PortStp='spanning_tree_state',
        )
    ),
    IpFwdNewCfgPortTable: dict(
        struct=PhysicalPortParameters,
        direct=True,
        attrs=dict(
            Index='index',
            State='ip_forwarding'
        )
    )
}

bean_state_map = {
    PortInfoTable: dict(exclude=['PhyIfLastChange'])
}
bean_stats_map = {
    PortStatsTable: dict()
}


class PhysicalPortConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[PhysicalPortParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map
    stats_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_stats_map

    def __init__(self, alteon_connection):
        super(PhysicalPortConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: PhysicalPortParameters) -> PhysicalPortParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: PhysicalPortParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: PhysicalPortParameters, dry_run=False, **kw) -> str:
        return MSG_NO_DELETE

    def clear_stats(self, parameters: PhysicalPortParameters, **kw) -> str:
        bean = PortStatsTable()
        bean.Indx = parameters.index
        bean.Clear = EnumPortStatsClear.clear
        self._device_api.update(bean)
        return 'Port {0} statistics cleared'.format(parameters.index)

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(AgPortNewCfgTable, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_all_props = True
        return dry_run_procedure
