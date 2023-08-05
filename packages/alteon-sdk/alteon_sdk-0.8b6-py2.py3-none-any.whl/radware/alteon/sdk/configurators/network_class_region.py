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

from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.SlbNewNwclssCfgNetworkClassesTable import *
from radware.alteon.beans.SlbNewNwclssCfgNetworkElementsTable import *

from typing import List, Optional, Union, ClassVar


class RegionContinent(RadwareParametersExtension):
    africa = 'Africa'
    antarctica = 'Antarctica'
    asia = 'Asia'
    europe = 'Europe'
    north_america = 'North America'
    oceania = 'Oceania'
    south_america = 'South America'


class NetworkClassRegionEntry(RadwareParametersStruct):
    name: str
    region_continent: RegionContinent
    region_country: Optional[str]
    region_state: Optional[str]

    def __init__(self, index: str = None, region_continent: RegionContinent = None):
        self.name = index
        self.region_continent = region_continent
        self.region_country = None
        self.region_state = None


class NetworkClassRegionParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    classes: Optional[List[NetworkClassRegionEntry]]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.classes = list()


bean_map = {
    SlbNewNwclssCfgNetworkClassesTable: dict(
        struct=NetworkClassRegionParameters,
        direct=True,
        attrs=dict(
            Id='index',
            Name='description',
        )
    ),
    SlbNewNwclssCfgNetworkElementsTable: dict(
        struct=List[NetworkClassRegionEntry],
        direct=True,
        attrs=dict(
            NcId='index',
            Id='name',
            RegCont='region_continent',
            RegCountry='region_country',
            RegState='region_state'
        )
    )
}


class NetworkClassRegionConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[NetworkClassRegionParameters]

    def __init__(self, alteon_connection):
        super(NetworkClassRegionConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: NetworkClassRegionParameters) -> Union[NetworkClassRegionParameters, None]:
        self._read_device_beans(parameters)
        if self._beans:
            if self._beans:
                if self._beans[SlbNewNwclssCfgNetworkClassesTable].Type != EnumSlbNwclssNetworkClassesType.region:
                    return None
            return parameters

    def _update(self, parameters: NetworkClassRegionParameters, dry_run: bool) -> str:
        self._write_bean(SlbNewNwclssCfgNetworkClassesTable, parameters,
                         dict(Type=EnumSlbNwclssNetworkClassesType.region), dry_run=dry_run)
        # alteon need to create new entry first
        for x in range(2):
            self._write_bean_collection(SlbNewNwclssCfgNetworkElementsTable, parameters.classes,
                                        dict(NcId=parameters.index), dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewNwclssCfgNetworkClassesTable, parameters)

    def delete(self, parameters: NetworkClassRegionParameters, dry_run=False, **kw) -> str:
        ## must remove each indvidual net_class ip entry
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        self._validate_prepare_parameters(parameters)
        cur_params = NetworkClassRegionParameters()
        cur_params.index = parameters.index
        self._read_device_beans(cur_params)
        for entry in cur_params.classes:
            instance = self._get_bean_instance(SlbNewNwclssCfgNetworkElementsTable, entry)
            instance.NcId = parameters.index
            self._device_api.delete(instance, dry_run=dry_run)
        self_obj = self._entry_bean_instance(parameters)
        self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

    def _update_remove(self, parameters: NetworkClassRegionParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.classes, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE
