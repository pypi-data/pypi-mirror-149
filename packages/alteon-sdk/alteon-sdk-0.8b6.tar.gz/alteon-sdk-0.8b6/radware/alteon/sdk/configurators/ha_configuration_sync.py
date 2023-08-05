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
from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from radware.alteon.beans.SlbNewCfgPeerTable import *
from typing import List, Optional, ClassVar


class SyncPeerParameters(RadwareParametersStruct):
    state: Optional[EnumSlbPeerState]
    ip_ver: Optional[EnumSlbPeerIpVersion]
    ip4_address: Optional[str]
    ip6_address: Optional[str]

    def __init__(self):
        self.state = None
        self.ip_ver = None
        self.ip4_address = None
        self.ip6_address = None


class ConfigurationSyncParameters(RadwareParametersStruct):
    automatic_sync: Optional[EnumSlbNewCfgSyncAutosync]
    filter_sync: Optional[EnumSlbNewCfgSyncFilt]
    ip_interface_sync: Optional[EnumSlbNewCfgSyncL3]
    port_sync: Optional[EnumSlbNewCfgSyncPort]
    gateway_sync: Optional[EnumSlbNewCfgSyncGw]
    bandwidth_management_sync: Optional[EnumSlbNewCfgSyncBwm]
    vrrp_sync: Optional[EnumSlbNewCfgSyncVrrp]
    proxy_ip_sync: Optional[EnumSlbNewCfgSyncPip]
    peer_proxy_ip_sync: Optional[EnumSlbNewCfgSyncPeerPip]
    static_route_sync: Optional[EnumSlbNewCfgSyncRoute]
    certificate_sync: Optional[EnumSlbNewCfgSyncCerts]
    mapping_only_sync: Optional[EnumSlbNewCfgSyncMaponly]
    certificate_passphrase: Optional[PasswordArgument]
    peer_authentication_mode: Optional[EnumSlbNewCfgSyncPasswordMode]
    authentication_passphrase: Optional[PasswordArgument]
    sync_peers: Optional[List[SyncPeerParameters]]

    def __init__(self):
        self.automatic_sync = None
        self.filter_sync = None
        self.ip_interface_sync = None
        self.port_sync = None
        self.gateway_sync = None
        self.bandwidth_management_sync = None
        self.vrrp_sync = None
        self.proxy_ip_sync = None
        self.peer_proxy_ip_sync = None
        self.static_route_sync = None
        self.certificate_sync = None
        self.mapping_only_sync = None
        self.certificate_passphrase = None
        self.peer_authentication_mode = None
        self.authentication_passphrase = None
        self.sync_peers = list()


bean_map = {
    Root: dict(
        struct=ConfigurationSyncParameters,
        direct=True,
        attrs=dict(
            slbNewCfgSyncAutosync='automatic_sync',
            slbNewCfgSyncFilt='filter_sync',
            slbNewCfgSyncL3='ip_interface_sync',
            slbNewCfgSyncPort='port_sync',
            slbNewCfgSyncGw='gateway_sync',
            slbNewCfgSyncBwm='bandwidth_management_sync',
            slbNewCfgSyncVrrp='vrrp_sync',
            slbNewCfgSyncPip='proxy_ip_sync',
            slbNewCfgSyncPeerPip='peer_proxy_ip_sync',
            slbNewCfgSyncRoute='static_route_sync',
            slbNewCfgSyncCerts='certificate_sync',
            slbNewCfgSyncMaponly='mapping_only_sync',
            slbNewCfgSyncCertsPassPhrase='certificate_passphrase',
            slbNewCfgSyncCertsConfPassPhrase='certificate_passphrase',
            slbNewCfgSyncPasswordMode='peer_authentication_mode',
            slbCfgSyncPassphrase='authentication_passphrase'
        )
    ),
    SlbNewCfgPeerTable: dict(
        struct=List[SyncPeerParameters],
        direct=True,
        attrs=dict(
            State='state',
            IpVersion='ip_ver',
            IpAddr='ip4_address',
            Ipv6Addr='ip6_address'
        )
    )
}
auto_write_exception = [SlbNewCfgPeerTable]


class ConfigurationSyncConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[ConfigurationSyncParameters]

    def __init__(self, alteon_connection):
        super(ConfigurationSyncConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: ConfigurationSyncParameters) -> ConfigurationSyncParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: ConfigurationSyncParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)
        self._assign_write_numeric_index_beans(SlbNewCfgPeerTable, parameters.sync_peers, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: ConfigurationSyncParameters, dry_run=False, **kw):
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        peers = self._device_api.read_all(SlbNewCfgPeerTable())
        for peer in peers:
            self._device_api.delete(peer, dry_run=dry_run)
        return 'sync peers' + MSG_DELETE

    def _update_remove(self, parameters: ConfigurationSyncParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.sync_peers, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        return dry_run_procedure

