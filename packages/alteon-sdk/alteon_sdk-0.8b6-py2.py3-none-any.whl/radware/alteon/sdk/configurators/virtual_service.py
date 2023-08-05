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
from radware.alteon.beans.SlbNewCfgEnhVirtServicesTable import *
from radware.alteon.beans.SlbNewCfgEnhVirtServicesSecondPartTable import *
from radware.alteon.beans.SlbNewCfgEnhVirtServicesFifthPartTable import *
from radware.alteon.beans.SlbNewCfgEnhVirtServicesSixthPartTable import *
from radware.alteon.beans.SlbNewCfgEnhVirtServicesSeventhPartTable import *
from radware.alteon.beans.SlbEnhStatVirtServiceTable import SlbEnhStatVirtServiceTable
from radware.alteon.beans.SlbStatEnhContRuleActionGroupTable import SlbStatEnhContRuleActionGroupTable
from radware.alteon.beans.SlbNewCfgEnhSerAppShapeTable import *
from typing import Optional, ClassVar, Dict, List


class AppshapeEntry(RadwareParametersStruct):
    priority: int
    name: Optional[str]

    def __init__(self, priority: int = None):
        self.priority = priority
        self.name = None


class VirtualServiceParameters(RadwareParametersStruct):
    index: str
    service_index: int
    description: Optional[str]
    service_port: Optional[int]
    server_port: Optional[int]
    protocol: Optional[EnumSlbVirtServiceUDPBalance]
    direct_server_return: Optional[EnumSlbVirtServiceDirServerRtn]
    persistent_mode: Optional[EnumSlbVirtServicePBind]
    cookie_mode: Optional[EnumSlbVirtServiceCookieMode]
    delayed_binding: Optional[EnumSlbVirtServiceDBind]
    ssl_policy_name: Optional[str]
    server_cert_name: Optional[str]
    http_mod_policy_name: Optional[str]
    application_type: Optional[EnumSlbVirtServApplicationType]
    service_action: Optional[EnumSlbVirtServiceAction]
    redirect_location: Optional[str]
    server_cert_type: Optional[EnumSlbVirtServiceServCertGrpMark]
    cookie_path: Optional[str]
    secure_cookie: Optional[EnumSlbVirtServiceCookieSecure]
    log_sessions: Optional[EnumSlbVirtServiceSessLog]
    service_always_on_with_appshape: Optional[EnumSlbVirtServiceAlwaysOn]
    service_down_connection: Optional[EnumSlbVirtServiceSendRST]
    cookie_id: Optional[str]
    direct_access_mode: Optional[EnumSlbVirtServiceDirect]
    x_fwd_for_inject: Optional[EnumSlbVirtServiceXForwardedFor]
    persistent_server_port: Optional[EnumSlbVirtServicePbindRport]
    cookie_insert_domain_name: Optional[EnumSlbVirtServiceCookieDname]
    connection_idle_timeout_minutes: Optional[int]
    server_group_name: Optional[str]
    session_mirror: Optional[EnumSlbVirtServiceSessionMirror]
    persistent_timeout_minutes: Optional[int]
    nat_mode: Optional[EnumSlbVirtServiceProxyIpMode]
    nat_address: Optional[str]
    nat_subnet: Optional[str]
    nat6_address: Optional[str]
    nat6_prefix: Optional[int]
    nat_ip_persistency: Optional[EnumSlbVirtServiceProxyIpPersistency]
    nat_network_class_name: Optional[str]
    nat_net_class_ip_persistency: Optional[EnumSlbVirtServiceProxyIpNWclassPersistency]
    close_connection_with_reset: Optional[EnumSlbVirtServiceClsRST]
    cluster_mode: Optional[EnumSlbVirtServiceCluster]
    gslb_http_redirect: Optional[EnumSlbVirtServiceHttpRedir]
    appshapes: Optional[List[AppshapeEntry]]

    def __init__(self, index: str = None, service_index: int = None):
        self.index = index
        self.service_index = service_index
        self.description = None
        self.service_port = None
        self.server_port = None
        self.protocol = None
        self.direct_server_return = None
        self.persistent_mode = None
        self.cookie_mode = None
        self.delayed_binding = None
        self.ssl_policy_name = None
        self.server_cert_name = None
        self.http_mod_policy_name = None
        self.application_type = None
        self.service_action = None
        self.redirect_location = None
        self.server_cert_type = None
        self.cookie_path = None
        self.secure_cookie = None
        self.log_sessions = None
        self.service_always_on_with_appshape = None
        self.service_down_connection = None
        self.cookie_id = None
        self.direct_access_mode = None
        self.x_fwd_for_inject = None
        self.persistent_server_port = None
        self.cookie_insert_domain_name = None
        self.connection_idle_timeout_minutes = None
        self.server_group_name = None
        self.session_mirror = None
        self.persistent_timeout_minutes = None
        self.nat_mode = None
        self.nat_address = None
        self.nat_subnet = None
        self.nat6_address = None
        self.nat6_prefix = None
        self.nat_ip_persistency = None
        self.nat_network_class_name = None
        self.nat_net_class_ip_persistency = None
        self.close_connection_with_reset = None
        self.cluster_mode = None
        self.gslb_http_redirect = None
        self.appshapes = list()


bean_map = {
    SlbNewCfgEnhVirtServicesTable: dict(
        struct=VirtualServiceParameters,
        direct=True,
        attrs=dict(
            ServIndex='index',
            Index='service_index',
            VirtPort='service_port',
            RealPort='server_port',
            UDPBalance='protocol',
            DirServerRtn='direct_server_return',
            PBind='persistent_mode',
            CookieMode='cookie_mode',
            DBind='delayed_binding'
        )
    ),
    SlbNewCfgEnhVirtServicesSecondPartTable: dict(
        struct=VirtualServiceParameters,
        direct=True,
        attrs=dict(
            ServSecondPartIndex='index',
            SecondPartIndex='service_index',
            SSLpol='ssl_policy_name',
            ServCert='server_cert_name',
            HttpmodList='http_mod_policy_name'
        )
    ),
    SlbNewCfgEnhVirtServicesFifthPartTable: dict(
        struct=VirtualServiceParameters,
        direct=True,
        attrs=dict(
            ServFifthPartIndex='index',
            FifthPartIndex='service_index',
            ServApplicationType='application_type',
            Action='service_action',
            Redirect='redirect_location',
            ServCertGrpMark='server_cert_type',
            CookiePath='cookie_path',
            CookieSecure='secure_cookie',
            SessLog='log_sessions',
            AlwaysOn='service_always_on_with_appshape',
            SendRST='service_down_connection',
            Name='description'
        )
    ),
    SlbNewCfgEnhVirtServicesSixthPartTable: dict(
        struct=VirtualServiceParameters,
        direct=True,
        attrs=dict(
            ServSixthPartIndex='index',
            SixthPartIndex='service_index',
            Cname='cookie_id',
            Direct='direct_access_mode',
            XForwardedFor='x_fwd_for_inject',
            PbindRport='persistent_server_port',
            CookieDname='cookie_insert_domain_name',
            TimeOut='connection_idle_timeout_minutes',
            HttpRedir='gslb_http_redirect'
        )
    ),
    SlbNewCfgEnhVirtServicesSeventhPartTable: dict(
        struct=VirtualServiceParameters,
        direct=True,
        attrs=dict(
            ServSeventhPartIndex='index',
            SeventhPartIndex='service_index',
            RealGroup='server_group_name',
            SessionMirror='session_mirror',
            PersistentTimeOut='persistent_timeout_minutes',
            ProxyIpMode='nat_mode',
            ProxyIpAddr='nat_address',
            ProxyIpMask='nat_subnet',
            ProxyIpv6Addr='nat6_address',
            ProxyIpv6Prefix='nat6_prefix',
            ProxyIpPersistency='nat_ip_persistency',
            ProxyIpNWclass='nat_network_class_name',
            ProxyIpNWclassPersistency='nat_net_class_ip_persistency',
            ClsRST='close_connection_with_reset',
            Cluster='cluster_mode'
        )
    ),
    SlbNewCfgEnhSerAppShapeTable: dict(
        struct=List[AppshapeEntry],
        direct=True,
        attrs=dict(
            VirtServIndex='index',
            VirtServiceIndex='service_index',
            Priority='priority',
            Index='name'
        )
    )
}

bean_state_map = {
    SlbEnhStatVirtServiceTable: dict(include=['ServerIndex', 'Index', 'RealServerIndex', 'RealStatus']),
    SlbStatEnhContRuleActionGroupTable: dict(include=['ActionVirtServIndex', 'ActionVirtServiceIndex', 'Index',
                                                      'EnhContActionRealServerIndex', 'RealStatus'])
}

auto_write_exception = [SlbNewCfgEnhSerAppShapeTable]


class VirtualServiceConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[VirtualServiceParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(VirtualServiceConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: VirtualServiceParameters) -> VirtualServiceParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: VirtualServiceParameters, dry_run: bool) -> str:
        parameters.clear_zero_ip_address()
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)
        if parameters.appshapes:
            for appshape in parameters.appshapes:
                instance = self._get_bean_instance(SlbNewCfgEnhSerAppShapeTable, parameters)
                instance.Index = appshape.name
                instance.Priority = appshape.priority
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: VirtualServiceParameters, dry_run: bool) -> str:
        instance = self._get_bean_instance(SlbNewCfgEnhSerAppShapeTable, parameters)
        as_indexes = [appshape.priority for appshape in parameters.appshapes]
        self._remove_device_beans_by_simple_collection(as_indexes, instance, 'Priority', dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgEnhVirtServicesTable, parameters)

