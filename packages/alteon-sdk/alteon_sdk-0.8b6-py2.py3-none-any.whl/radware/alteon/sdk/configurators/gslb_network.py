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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator, NumericConfigurator
from radware.alteon.beans.GslbNewCfgEnhNetworkTable import *
from radware.alteon.beans.GslbNewCfgEnhNetAlphaNumRealPrefTable import *
from radware.alteon.beans.GslbNewCfgEnhNetAlphaNumVirtPrefTable import *
from typing import List, Optional, ClassVar


class GSLBNetworkParameters(RadwareParametersStruct):
    index: int
    state: Optional[EnumGslbNetworkState]
    ip_ver: Optional[EnumGslbNetworkVer]
    src_address_type: Optional[EnumGslbNetworkSrcAddrType]
    src_network_address: Optional[str]
    src_network_subnet: Optional[str]
    src6_network_address: Optional[str]
    src6_network_prefix: Optional[int]
    src_network_class_id: Optional[str]
    src_lookup_mode: Optional[EnumGslbNetworkClientAddrSrc]
    nat_service_type: Optional[EnumGslbNetworkServType]
    wan_group_name: Optional[str]
    virtual_server_names: Optional[List[str]]
    server_names: Optional[List[str]]

    def __init__(self, index: int = None):
        self.index = index
        self.state = None
        self.ip_ver = None
        self.src_address_type = None
        self.src_network_address = None
        self.src_network_subnet = None
        self.src6_network_address = None
        self.src6_network_prefix = None
        self.src_network_class_id = None
        self.src_lookup_mode = None
        self.nat_service_type = None
        self.wan_group_name = None
        self.virtual_server_names = list()
        self.server_names = list()


bean_map = {
    GslbNewCfgEnhNetworkTable: dict(
        struct=GSLBNetworkParameters,
        direct=True,
        attrs=dict(
            Indx='index',
            State='state',
            Ver='ip_ver',
            SourceIp='src_network_address',
            NetMask='src_network_subnet',
            SourceIpV6='src6_network_address',
            Sprefix='src6_network_prefix',
            ClassId='src_network_class_id',
            ClientAddrSrc='src_lookup_mode',
            SrcAddrType='src_address_type',
            ServType='nat_service_type',
            WanGrp='wan_group_name'
        )
    ),
    GslbNewCfgEnhNetAlphaNumRealPrefTable: dict(
        struct=List[GSLBNetworkParameters],
        direct=False,
        attrs=dict(
            Indx='index'
        )
    ),
    GslbNewCfgEnhNetAlphaNumVirtPrefTable: dict(
        struct=List[GSLBNetworkParameters],
        direct=False,
        attrs=dict(
            Indx='index'
        )
    )
}


class GSLBNetworkConfigurator(AlteonConfigurator, NumericConfigurator):
    parameters_class: ClassVar[GSLBNetworkParameters]

    def __init__(self, alteon_connection):
        AlteonConfigurator.__init__(self, bean_map, alteon_connection)

    def _read(self, parameters: GSLBNetworkParameters) -> GSLBNetworkParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.server_names = list()
            parameters.virtual_server_names = list()
            for entry in self._beans[GslbNewCfgEnhNetAlphaNumRealPrefTable]:
                parameters.server_names.append(entry.ServerIndx)
            for entry in self._beans[GslbNewCfgEnhNetAlphaNumVirtPrefTable]:
                parameters.virtual_server_names.append(entry.ServerIndx)
            return parameters

    def _update(self, parameters: GSLBNetworkParameters, dry_run: bool) -> str:
        def _update_entry(resource_list, server_flag):
            if resource_list:
                for name in resource_list:
                    entry = self._get_bean_instance(GslbNewCfgEnhNetworkTable, parameters)
                    if server_flag:
                        entry.AddRealServerAlphaNum = name
                    else:
                        entry.AddEnhVirtServer = name
                    self._device_api.update(entry, dry_run=dry_run)

        parameters.clear_zero_ip_address()
        self._write_device_beans(parameters, dry_run=dry_run)
        _update_entry(parameters.server_names, True)
        _update_entry(parameters.virtual_server_names, False)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: GSLBNetworkParameters, dry_run: bool) -> str:
        instance = GslbNewCfgEnhNetAlphaNumRealPrefTable()
        instance.Indx = parameters.index
        self._remove_device_beans_by_simple_collection(parameters.server_names, instance, 'ServerIndx', dry_run=dry_run)
        instance = GslbNewCfgEnhNetAlphaNumVirtPrefTable()
        instance.Indx = parameters.index
        self._remove_device_beans_by_simple_collection(parameters.virtual_server_names, instance, 'ServerIndx',
                                                       dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(GslbNewCfgEnhNetworkTable, parameters)
