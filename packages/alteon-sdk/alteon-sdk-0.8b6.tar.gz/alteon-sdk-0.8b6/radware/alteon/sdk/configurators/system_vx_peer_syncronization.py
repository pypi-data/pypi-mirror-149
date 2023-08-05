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
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from radware.alteon.beans.AgSysPeerNewCfgTable import *
from typing import List, Optional, ClassVar


class PeerSwitchEntry(RadwareParametersStruct):
    id: int
    ip4_address: Optional[str]
    ip6_address: Optional[str]
    ip_ver: Optional[EnumAgSysPeerAddrType]
    state: Optional[EnumAgSysPeerState]
    vadc_ids: Optional[List[int]]

    def __init__(self, peer_id: int = None):
        self.id = peer_id
        self.ip4_address = None
        self.ip6_address = None
        self.ip_ver = None
        self.state = None
        self.vadc_ids = list()

    def struct_normalization(self):
        if self.vadc_ids is not None and type(self.vadc_ids) == str:
            self.vadc_ids = BeanUtils.decode_bmp_sub_one(self.vadc_ids)


class VXPeerSyncParameters(RadwareParametersStruct):
    auto_sync: Optional[EnumAgSysNewSyncAutosync]
    sync_authentication_mode: Optional[EnumAgSysNewSyncPasswordMode]
    sync_authentication_passphrase: Optional[PasswordArgument]
    peer_switches: Optional[List[PeerSwitchEntry]]

    def __init__(self):
        self.auto_sync = None
        self.sync_authentication_mode = None
        self.sync_authentication_passphrase = None
        self.peer_switches = list()


bean_map = {
    Root: dict(
        struct=VXPeerSyncParameters,
        direct=True,
        attrs=dict(
            agSysNewSyncAutosync='auto_sync',
            agSysNewSyncPasswordMode='sync_authentication_mode',
            agSysSyncPassphrase='sync_authentication_passphrase'
        )
    ),
    AgSysPeerNewCfgTable: dict(
        struct=List[PeerSwitchEntry],
        direct=True,
        attrs=dict(
            Index='id',
            Addr='ip4_address',
            Ipv6Addr='ip6_address',
            AddrType='ip_ver',
            State='state',
            VadcBmap='vadc_ids'
        )
    )
}


class VXPeerSyncConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[VXPeerSyncParameters]

    def __init__(self, alteon_connection):
        super(VXPeerSyncConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: VXPeerSyncParameters) -> VXPeerSyncParameters:
        if not self._mng_info.is_vx:
            raise DeviceConfiguratorError(self.__class__, 'not a VX container')

        self._read_device_beans(parameters)
        if self._beans:
            for peer_sw in parameters.peer_switches:
                peer_sw.vadc_ids = BeanUtils.decode_bmp_sub_one(peer_sw.vadc_ids)
            return parameters

    def _update(self, parameters: VXPeerSyncParameters, dry_run: bool) -> str:
        if not self._mng_info.is_vx:
            raise DeviceConfiguratorError(self.__class__, 'not a VX container')

        for peer_sw in parameters.peer_switches:
            if peer_sw.vadc_ids is not None:
                for vadc_id in peer_sw.vadc_ids:
                    peer_entry = self._get_bean_instance(AgSysPeerNewCfgTable, peer_sw)
                    peer_entry.VadcAdd = vadc_id
                    self._device_api.update(peer_entry, dry_run=dry_run)
            peer_sw.vadc_ids = None

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: VXPeerSyncParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        if not self._mng_info.is_vx:
            raise DeviceConfiguratorError(self.__class__, 'not a VX container')

        for peer_entry in self._device_api.read_all(AgSysPeerNewCfgTable()):
            self._device_api.delete(peer_entry, dry_run=dry_run)

        return 'vx sync peers' + MSG_DELETE

    def _update_remove(self, parameters: VXPeerSyncParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.peer_switches, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        if 'peer_switches' in diff:
            peers = list()
            for item in diff['peer_switches']:
                if item['ip4_address'] != '0.0.0.0' or \
                        item['ip6_address'] or \
                        item['ip_ver'] != 'ipv4' or \
                        item['state'] != 'disabled' or item['vadc_ids']:
                    peers.append(item)
            if peers:
                diff['peer_switches'] = peers
            else:
                diff.pop('peer_switches')
        return dry_run_procedure

