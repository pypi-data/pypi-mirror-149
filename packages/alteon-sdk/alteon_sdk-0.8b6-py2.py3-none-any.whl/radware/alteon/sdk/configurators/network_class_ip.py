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
from radware.alteon.beans.SlbNewNwclssCfgNetworkClassesTable import *
from radware.alteon.beans.SlbNewNwclssCfgNetworkElementsTable import *

from typing import List, Optional, Union, ClassVar


class NetworkClassIPEntry(RadwareParametersStruct):
    name: str
    network_type: EnumSlbNwclssNetworkElementsNetType
    ip4_address: Optional[str]
    ip4_subnet: Optional[str]
    ip4_range_first_address: Optional[str]
    ip4_range_last_address: Optional[str]
    ip6_address: Optional[str]
    ip6_prefix: Optional[int]
    ip6_range_first_address: Optional[str]
    ip6_range_last_address: Optional[str]
    match_type: Optional[EnumSlbNwclssNetworkElementsMatchType]

    def __init__(self, name: str = None, network_type: EnumSlbNwclssNetworkElementsNetType = None):
        self.name = name
        self.network_type = network_type
        self.ip4_address = None
        self.ip4_subnet = None
        self.ip4_range_first_address = None
        self.ip4_range_last_address = None
        self.ip6_subnet = None
        self.ip6_prefix = None
        self.ip6_range_first_address = None
        self.ip6_range_last_address = None
        self.match_type = None


class NetworkClassIPParameters(RadwareParametersStruct):
    index: str
    ip_ver: EnumSlbNwclssNetworkClassesIpVer
    description: Optional[str]
    classes: Optional[List[NetworkClassIPEntry]]

    def __init__(self, index: str = None, ip_ver: EnumSlbNwclssNetworkClassesIpVer = None):
        self.index = index
        self.ip_ver = ip_ver
        self.description = None
        self.classes = list()


bean_map = {
    SlbNewNwclssCfgNetworkClassesTable: dict(
        struct=NetworkClassIPParameters,
        direct=True,
        attrs=dict(
            Id='index',
            Name='description',
            IpVer='ip_ver'
        )
    ),
    SlbNewNwclssCfgNetworkElementsTable: dict(
        struct=List[NetworkClassIPEntry],
        direct=True,
        attrs=dict(
            NcId='index',
            Id='name',
            NetType='network_type',
            MatchType='match_type',
            Ip='ip4_address',
            Mask='ip4_subnet',
            FromIp='ip4_range_first_address',
            ToIp='ip4_range_last_address',
            Ipv6Addr='ip6_subnet',
            PrefixLen='ip6_prefix',
            FromIpv6Addr='ip6_range_first_address',
            ToIpv6Addr='ip6_range_last_address',
        )
    )
}


class NetworkClassIPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[NetworkClassIPParameters]

    def __init__(self, alteon_connection):
        super(NetworkClassIPConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: NetworkClassIPParameters) -> Union[NetworkClassIPParameters, None]:
        self._read_device_beans(parameters)
        if self._beans:
            if self._beans[SlbNewNwclssCfgNetworkClassesTable].Type != EnumSlbNwclssNetworkClassesType.address:
                return None
            return parameters

    def _update(self, parameters: NetworkClassIPParameters, dry_run: bool) -> str:
        if parameters.classes:
            for c in parameters.classes:
                if c.ip6_prefix == 0:
                    c.ip6_prefix = None
        self._write_bean(SlbNewNwclssCfgNetworkClassesTable, parameters,
                         dict(Type=EnumSlbNwclssNetworkClassesType.address), dry_run=dry_run)
        # alteon need to create new entry first
        for x in range(2):
            self._write_bean_collection(SlbNewNwclssCfgNetworkElementsTable, parameters.classes,
                                        dict(NcId=parameters.index), dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewNwclssCfgNetworkClassesTable, parameters)

    def delete(self, parameters: NetworkClassIPParameters, dry_run=False, **kw) -> str:
        ## must remove each indvidual net_class ip entry
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        self._validate_prepare_parameters(parameters)
        cur_params = NetworkClassIPParameters()
        cur_params.index = parameters.index
        self._read_device_beans(cur_params)
        for entry in cur_params.classes:
            instance = self._get_bean_instance(SlbNewNwclssCfgNetworkElementsTable, entry)
            instance.NcId = parameters.index
            self._device_api.delete(instance, dry_run=dry_run)
        self_obj = self._entry_bean_instance(parameters)
        self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

    def _update_remove(self, parameters: NetworkClassIPParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.classes, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

