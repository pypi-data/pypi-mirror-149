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


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.BgpNewCfgPeerTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.configurators.bgp_global import *
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError


class BgpPeerParameters(RadwareParametersStruct):
    index: int
    remote_addr: Optional[str]
    remote_as_number: Optional[int]
    ttl: Optional[int]
    state: Optional[EnumBgpPeerState]
    advertised_route_metric: Optional[int]
    default_route_action: Optional[EnumBgpPeerDefaultAction]
    advertising_ospf_routes: Optional[EnumBgpPeerOspfState]
    advertising_fixed_routes: Optional[EnumBgpPeerFixedState]
    advertising_static_routes: Optional[EnumBgpPeerStaticState]
    advertising_vip_routes: Optional[EnumBgpPeerVipState]
    hold_time: Optional[int]
    keep_alive_time: Optional[int]
    min_adv_time: Optional[int]
    connect_retry_interval: Optional[int]
    min_as_origination_interval: Optional[int]
    advertising_rip_routes: Optional[EnumBgpPeerRipState]
    advertising_deny_routes: Optional[EnumBgpPeerDenyState]
    next_hop_addr: Optional[str]
    bfd: Optional[EnumBgpPeerBfdState]
    ip_version: Optional[EnumbgpNewCfgPeerIpVer]
    remote_ipv6_addr: Optional[str]
    in_rmap_list: Optional[List[int]]
    out_rmap_list: Optional[List[int]]
    graceful_restart_status: Optional[EnumBgpPeerGracefulState]
    standard_community_advertisement_status: Optional[EnumBgpPeerCommAdv]
    large_community_advertisement_status: Optional[EnumBgpPeerCommAdv]
    extended_community_advertisement_status: Optional[EnumBgpPeerCommAdv]
    ttl_security_hops: Optional[int]
    peer_password: Optional[str]
    password_status: Optional[EnumBgpPeerPasswordStatus]


    def __init__(self, index: int = None):
        self.index = index
        self.remote_addr = None
        self.remote_as_number = None
        self.ttl = None
        self.state = None
        self.advertised_route_metric = None
        self.default_route_action = None
        self.advertising_ospf_routes = None
        self.advertising_fixed_routes = None
        self.advertising_static_routes = None
        self.advertising_vip_routes = None
        self.hold_time = None
        self.keep_alive_time = None
        self.min_adv_time = None
        self.connect_retry_interval = None
        self.min_as_origination_interval = None
        self.advertising_rip_routes = None
        self.advertising_deny_routes = None
        self.next_hop_addr = None
        self.bfd = None
        self.ip_version = None
        self.remote_ipv6_addr = None
        self.in_rmap_list = list()
        self.out_rmap_list = list()
        self.graceful_restart_status = None
        self.standard_community_advertisement_status = None
        self.large_community_advertisement_status = None
        self.extended_community_advertisement_status = None
        self.ttl_security_hops = None
        self.peer_password = None
        self.password_status = None

bean_map = {
    BgpNewCfgPeerTable: dict(
        struct=BgpPeerParameters,
        direct=True,
        attrs=dict(
            Index='index',
            RemoteAddr='remote_addr',
            RemoteAs='remote_as_number',
            Ttl='ttl',
            State='state',
            Metric='advertised_route_metric',
            DefaultAction='default_route_action',
            OspfState='advertising_ospf_routes',
            FixedState='advertising_fixed_routes',
            StaticState='advertising_static_routes',
            VipState='advertising_vip_routes',
            HoldTime='hold_time',
            KeepAlive='keep_alive_time',
            MinTime='min_adv_time',
            ConRetry='connect_retry_interval',
            MinAS='min_as_origination_interval',
            RipState='advertising_rip_routes',
            DenyState='advertising_deny_routes',
            NextHop='next_hop_addr',
            BfdState='bfd',
            IpVer='ip_version',
            RemoteAddr6='remote_ipv6_addr',
            GracefulState='graceful_restart_status',
            StdCommAdv='standard_community_advertisement_status',
            LarCommAdv='large_community_advertisement_status',
            ExtCommAdv='extended_community_advertisement_status',
            SecureHops='ttl_security_hops',
            Password='peer_password',
            PasswordStatus='password_status'
        )
    )
}


class BgpPeerConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[BgpPeerParameters]

    def __init__(self, alteon_connection):
        super(BgpPeerConfigurator, self).__init__(bean_map, alteon_connection)        
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: BgpPeerParameters) -> BgpPeerParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.in_rmap_list = BeanUtils.decode_bmp(self._beans[BgpNewCfgPeerTable].InRmapList)
            parameters.out_rmap_list = BeanUtils.decode_bmp(self._beans[BgpNewCfgPeerTable].OutRmapList)
            return parameters

    def _update(self, parameters: BgpPeerParameters, dry_run: bool) -> str:
        self._VX_not_supported_field_validation(parameters)
        self._write_device_beans(parameters, dry_run=dry_run)
        if parameters.in_rmap_list:
            for in_rmap_idx in parameters.in_rmap_list:
                if in_rmap_idx!=0:
                    instance = self._get_bean_instance(BgpNewCfgPeerTable, parameters)
                    instance.AddInRmap = in_rmap_idx
                    self._device_api.update(instance, dry_run=dry_run)

        if parameters.out_rmap_list:
            for out_rmap_idx in parameters.out_rmap_list:
                if out_rmap_idx!=0:
                    instance = self._get_bean_instance(BgpNewCfgPeerTable, parameters)
                    instance.AddOutRmap = out_rmap_idx
                    self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: BgpPeerParameters, dry_run: bool) -> str:
        if parameters.in_rmap_list:
            instance = self._get_bean_instance(BgpNewCfgPeerTable, parameters)
            for in_rmap_idx in parameters.in_rmap_list:
                instance.RemoveInRmap = in_rmap_idx
                self._device_api.update(instance, dry_run=dry_run)

        if parameters.out_rmap_list:
            instance = self._get_bean_instance(BgpNewCfgPeerTable, parameters)
            for out_rmap_idx in parameters.out_rmap_list:
                instance.RemoveOutRmap = out_rmap_idx
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(BgpNewCfgPeerTable, parameters)

    def _VX_not_supported_field_validation(self, parameters):
        if self._mng_info.is_vadc:
            if parameters.graceful_restart_status is not None:
                raise DeviceConfiguratorError(self.__class__, 'graceful_restart_status is not supported on VADC instance')
            if parameters.ip_version is not None:
                raise DeviceConfiguratorError(self.__class__, 'ip_version is not supported on VADC instance')
            if parameters.remote_ipv6_addr is not None:
                raise DeviceConfiguratorError(self.__class__, 'remote_ipv6_addr is not supported on VADC instance')
            if parameters.standard_community_advertisement_status is not None:
                raise DeviceConfiguratorError(self.__class__, 'standard_community_advertisement_status is not supported on VADC instance')
            if parameters.large_community_advertisement_status is not None:
                raise DeviceConfiguratorError(self.__class__, 'large_community_advertisement_status is not supported on VADC instance')
            if parameters.extended_community_advertisement_status is not None:
                raise DeviceConfiguratorError(self.__class__, 'extended_community_advertisement_status is not supported on VADC instance')
            if parameters.ttl_security_hops is not None:
                raise DeviceConfiguratorError(self.__class__, 'ttl_security_hops is not supported on VADC instance')
            if parameters.peer_password is not None:
                raise DeviceConfiguratorError(self.__class__, 'peer_password is not supported on VADC instance')
            if parameters.password_status is not None:
                raise DeviceConfiguratorError(self.__class__, 'password_status is not supported on VADC instance')

