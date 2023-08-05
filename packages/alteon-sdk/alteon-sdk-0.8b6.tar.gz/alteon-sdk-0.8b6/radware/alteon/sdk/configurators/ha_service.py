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
# @author: Nofar Livkind, Radware


from typing import List, Optional, ClassVar
from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.HaServiceNewCfgTable import *
from radware.alteon.beans.HaServiceVipTable import *
from radware.alteon.beans.HaServiceFipTable import *
from radware.alteon.beans.HaServiceAdvIfsTable import *
from radware.alteon.beans.HaServiceTriggerGwNewCfgTable import *
from radware.alteon.beans.HaServiceTrackGwsTable import *
from radware.alteon.beans.HaServiceTriggerIfsNewCfgTable import *
from radware.alteon.beans.HaServiceTrackIfsTable import *
from radware.alteon.beans.HaServiceTriggerRealNewCfgTable import *
from radware.alteon.beans.HaServiceRealTable import *


class HaServiceParameters(RadwareParametersStruct):
    index: str
    pref: Optional[EnumHaServicePref]
    failBackMode: Optional[EnumHaServiceFailBackMode]
    advertise_Interval: Optional[int]
    interfaces: Optional[List[int]]
    floating_IPs: Optional[List[str]]
    vips: Optional[List[str]]
    state: Optional[EnumHaServiceState]
    trig_gwtrck_state: Optional[EnumHaServiceNewCfgTrigGwTrackState]
    trig_gwtrck_list: Optional[List[int]]
    trig_ifs_list: Optional[List[int]]
    trig_reals_state: Optional[EnumHaServiceNewCfgTrigRealTrkState]
    trig_reals_list: Optional[List[str]]

    def __init__(self, index: str = None):
        self.index = index
        self.pref = None
        self.failBackMode = None
        self.advertise_Interval = None
        self.interfaces = None
        self.floating_IPs = None
        self.vips = None
        self.state = None
        self.trig_gwtrck_state = None
        self.trig_gwtrck_list = None
        self.trig_ifs_list = None
        self.trig_reals_state = None
        self.trig_reals_list = None


bean_map = {
    HaServiceNewCfgTable: dict(
        struct=HaServiceParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Pref='pref',
            FailBackMode='failBackMode',
            Adver='advertise_Interval',
            State='state'
        )
    ),
    HaServiceVipTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index'
        )
    ),
    HaServiceFipTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index'
        )
    ),
    HaServiceAdvIfsTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
        )
    ),
    HaServiceTriggerGwNewCfgTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
            NewCfgTrigGwTrackState='trig_gwtrck_state'
        )
    ),
    HaServiceTrackGwsTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
        )
    ),
    HaServiceTriggerIfsNewCfgTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
        )
    ),
    HaServiceTrackIfsTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
        )
    ),
    HaServiceTriggerRealNewCfgTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
            NewCfgTrigRealTrkState='trig_reals_state'
        )
    ),
    HaServiceRealTable: dict(
        struct=List[HaServiceParameters],
        direct=False,
        attrs=dict(
            Index='index',
        )
    )
}


class HaServiceConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[HaServiceParameters]

    def __init__(self, alteon_connection):
        super(HaServiceConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: HaServiceParameters) -> HaServiceParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.interfaces = list()
            for interface in self._beans[HaServiceAdvIfsTable]:
                parameters.interfaces.append(interface.AdvIfIndex)
            parameters.floating_IPs = list()
            for fip in self._beans[HaServiceFipTable]:
                parameters.floating_IPs.append(fip.FipIndex)
            parameters.vips = list()
            for vip in self._beans[HaServiceVipTable]:
                parameters.vips.append(vip.HaServiceVipIndex)

            parameters.trig_gwtrck_list = list()
            for gw in self._beans[HaServiceTrackGwsTable]:
                parameters.trig_gwtrck_list.append(gw.TrackGwIndex)

            parameters.trig_reals_list = list()
            for real in self._beans[HaServiceRealTable]:
                parameters.trig_reals_list.append(real.Index)

            parameters.trig_ifs_list = list()
            for ifs in self._beans[HaServiceTrackIfsTable]:
                parameters.trig_ifs_list.append(ifs.TrackIfIndex)

            parameters.trig_gwtrck_state = self._beans[HaServiceTriggerGwNewCfgTable][0].NewCfgTrigGwTrackState
            parameters.trig_reals_state = self._beans[HaServiceTriggerRealNewCfgTable][0].NewCfgTrigRealTrkState

            return parameters

    def _update(self, parameters: HaServiceParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        instance = self._get_bean_instance(HaServiceNewCfgTable, parameters)
        instance_trig_gwtrck = self._get_bean_instance(HaServiceTriggerGwNewCfgTable, parameters)
        instance_trig_ifs = self._get_bean_instance(HaServiceTriggerIfsNewCfgTable, parameters)
        instance_trig_reals = self._get_bean_instance(HaServiceTriggerRealNewCfgTable, parameters)

        if parameters.interfaces:
            for interface in parameters.interfaces:
                instance.AddIf = interface
                self._device_api.update(instance, dry_run=dry_run)
        if parameters.floating_IPs:
            for floatIP in parameters.floating_IPs:
                instance.AddFip = floatIP
                self._device_api.update(instance, dry_run=dry_run)
        if parameters.vips:
            for vip in parameters.vips:
                instance.AddVip = vip
                self._device_api.update(instance, dry_run=dry_run)

        if parameters.trig_gwtrck_list:
            for gw in parameters.trig_gwtrck_list:
                instance_trig_gwtrck.NewCfgTrigGwTrackAdd = gw
                self._device_api.update(instance_trig_gwtrck, dry_run=dry_run)

        if parameters.trig_gwtrck_state != instance_trig_gwtrck.NewCfgTrigGwTrackState:
            instance_trig_gwtrck.NewCfgTrigGwTrackState = parameters.trig_gwtrck_state
            self._device_api.update(instance_trig_gwtrck, dry_run=dry_run)

        if parameters.trig_reals_list:
            for real in parameters.trig_reals_list:
                instance_trig_reals.NewCfgTrigAddReals = real
                self._device_api.update(instance_trig_reals, dry_run=dry_run)

        if parameters.trig_reals_state != instance_trig_reals.NewCfgTrigRealTrkState:
            instance_trig_reals.NewCfgTrigRealTrkState = parameters.trig_reals_state
            self._device_api.update(instance_trig_reals, dry_run=dry_run)

        if parameters.trig_ifs_list:
            for ifs in parameters.trig_ifs_list:
                instance_trig_ifs.NewCfgTrigIfTrackAdd = ifs
                self._device_api.update(instance_trig_ifs, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: HaServiceParameters, dry_run: bool) -> str:
        instance = self._get_bean_instance(HaServiceNewCfgTable, parameters)
        instance_trig_gwtrck = self._get_bean_instance(HaServiceTriggerGwNewCfgTable, parameters)
        instance_trig_ifs = self._get_bean_instance(HaServiceTriggerIfsNewCfgTable, parameters)
        instance_trig_reals = self._get_bean_instance(HaServiceTriggerRealNewCfgTable, parameters)

        if parameters.interfaces:
            for interface in parameters.interfaces:
                instance.RemIf = interface
                self._device_api.update(instance, dry_run=dry_run)
        if parameters.floating_IPs:
            for floatIP in parameters.floating_IPs:
                instance.RemFip = floatIP
                self._device_api.update(instance, dry_run=dry_run)
        if parameters.vips:
            for vip in parameters.vips:
                instance.RemVip = vip
                self._device_api.update(instance, dry_run=dry_run)

        if parameters.trig_gwtrck_list:
            for gw in parameters.trig_gwtrck_list:
                instance_trig_gwtrck.NewCfgTrigGwTrackExclude = gw
                self._device_api.update(instance_trig_gwtrck, dry_run=dry_run)

        if parameters.trig_reals_list:
            for real in parameters.trig_reals_list:
                instance_trig_reals.NewCfgTrigRemReals = real
                self._device_api.update(instance_trig_reals, dry_run=dry_run)

        if parameters.trig_ifs_list:
            for ifs in parameters.trig_ifs_list:
                instance_trig_ifs.NewCfgTrigIfTrackExclude = ifs
                self._device_api.update(instance_trig_ifs, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(HaServiceNewCfgTable, parameters)
