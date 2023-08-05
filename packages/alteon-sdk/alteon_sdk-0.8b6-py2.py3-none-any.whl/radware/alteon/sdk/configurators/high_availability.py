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


from typing import List, Optional, ClassVar
from radware.sdk.configurator import DryRunDeleteProcedure
from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *


class HighAvailabilityParameters(RadwareParametersStruct):
    mode: Optional[EnumHaNewCfgMode]
    advertise_bgp_routes_on_backup: Optional[EnumHaNewCfgBkpVipRt]
    holdoff_timer_second: Optional[int]
    send_garp_nwclss_proxy_ips: Optional[EnumHaNewCfgNwClGarp]
    advertisement_interval_second: Optional[int]
    fail_back_mode: Optional[EnumHaSwitchNewCfgFailBackMode]
    preferred_state: Optional[EnumHaSwitchNewCfgPref]
    gateway_tracking_state: Optional[EnumHaSwitchNewCfgTrigGwTrackState]
    real_server_tracking_state: Optional[EnumHaSwitchNewCfgTriggerl4Reals]
    sync_dynamic_data_store: Optional[EnumSlbNewCfgSyncDynamicData]
    sync_persistent_sessions: Optional[EnumSlbNewCfgSyncSfo]
    sync_session_interval_seconds: Optional[int]
    unicast_session_mirroring: Optional[EnumSlbNewCfgSyncUcastSfo]
    mirroring_primary_interface: Optional[int]
    mirroring_secondary_interface: Optional[int]
    cluster_master_election_priority: Optional[int]
    advertising_interfaces: Optional[List[int]]
    tracked_interfaces: Optional[List[int]]
    tracked_gateways: Optional[List[int]]

    def __init__(self):
        self.mode = None
        self.advertise_bgp_routes_on_backup = None
        self.holdoff_timer_second = None
        self.send_garp_nwclss_proxy_ips = None
        self.advertisement_interval_second = None
        self.fail_back_mode = None
        self.preferred_state = None
        self.gateway_tracking_state = None
        self.real_server_tracking_state = None
        self.sync_dynamic_data_store = None
        self.sync_persistent_sessions = None
        self.sync_session_interval_seconds = None
        self.unicast_session_mirroring = None
        self.mirroring_primary_interface = None
        self.mirroring_secondary_interface = None
        self.cluster_master_election_priority = None
        self.advertising_interfaces = list()
        self.tracked_interfaces = list()
        self.tracked_gateways = list()


bean_map = {
    Root: dict(
        struct=HighAvailabilityParameters,
        direct=True,
        attrs=dict(
            haNewCfgMode='mode',
            haNewCfgBkpVipRt='advertise_bgp_routes_on_backup',
            haNewCfgHoldoffTime='holdoff_timer_second',
            haNewCfgNwClGarp='send_garp_nwclss_proxy_ips',
            haSwitchNewCfgAdver='advertisement_interval_second',
            haSwitchNewCfgFailBackMode='fail_back_mode',
            haSwitchNewCfgPref='preferred_state',
            haSwitchNewCfgTrigGwTrackState='gateway_tracking_state',
            haSwitchNewCfgTriggerl4Reals='real_server_tracking_state',
            slbNewCfgSyncDynamicData='sync_dynamic_data_store',
            slbNewCfgSyncSfo='sync_persistent_sessions',
            slbNewCfgSyncSfoUpdatePeriod='sync_session_interval_seconds',
            slbNewCfgSyncUcastSfo='unicast_session_mirroring',
            slbNewCfgSyncUcastSfoPrimif='mirroring_primary_interface',
            slbNewCfgSyncUcastSfoSecif='mirroring_secondary_interface',
            haSwitchNewCfgOrder='cluster_master_election_priority',
            haSwitchNewCfgAdvIfsMapList='advertising_interfaces',
            haSwitchNewCfgTrackIfsMapList='tracked_interfaces',
            haSwitchNewCfgTrackGwsMapList='tracked_gateways'
        )
    )
}


class HighAvailabilityConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[HighAvailabilityParameters]

    def __init__(self, alteon_connection):
        super(HighAvailabilityConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: HighAvailabilityParameters) -> HighAvailabilityParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.advertising_interfaces = BeanUtils.decode_bmp(parameters.advertising_interfaces)
            parameters.tracked_interfaces = BeanUtils.decode_bmp(parameters.tracked_interfaces)
            parameters.tracked_gateways = BeanUtils.decode_bmp(parameters.tracked_gateways)
            return parameters

    def _update(self, parameters: HighAvailabilityParameters, dry_run: bool) -> str:
        if parameters.mode is not None:
            if EnumHaNewCfgMode.vrrp == parameters.mode:
                raise DeviceConfiguratorError(self.__class__, 'HA mode {0} not supported'.format(parameters.mode))

            self._update_ha_state(parameters.mode, dry_run=dry_run)

        self._update_advertise_track_objects(parameters.advertising_interfaces, 'haSwitchNewCfgAddIf', dry_run)
        self._update_advertise_track_objects(parameters.tracked_interfaces, 'haSwitchNewCfgTrigIfTrackAdd', dry_run)
        self._update_advertise_track_objects(parameters.tracked_gateways, 'haSwitchNewCfgTrigGwTrackAdd', dry_run)
        parameters.advertising_interfaces = None
        parameters.tracked_interfaces = None
        parameters.tracked_gateways = None

        if parameters.mode == EnumHaNewCfgMode.disabled:
            parameters.real_server_tracking_state = None

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: HighAvailabilityParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        self._update_ha_state(EnumHaNewCfgMode.switch, dry_run=dry_run)
        current = self.read(HighAvailabilityParameters())
        self._update_advertise_track_objects(current.advertising_interfaces, 'haSwitchNewCfgRemIf', dry_run)
        self._update_advertise_track_objects(current.tracked_interfaces, 'haSwitchNewCfgTrigIfTrackExclude', dry_run)
        self._update_advertise_track_objects(current.tracked_gateways, 'haSwitchNewCfgTrigGwTrackExclude', dry_run)

        current = HighAvailabilityParameters()
        current.mode = EnumHaNewCfgMode.switch
        current.preferred_state = EnumHaSwitchNewCfgPref.standby
        current.advertising_interfaces = None
        current.tracked_interfaces = None
        current.tracked_gateways = None
        current.fail_back_mode = EnumHaSwitchNewCfgFailBackMode.onfailure
        current.holdoff_timer_second = 0
        current.advertisement_interval_second = 1
        current.advertise_bgp_routes_on_backup = EnumHaNewCfgBkpVipRt.disabled
        current.send_garp_nwclss_proxy_ips = EnumHaNewCfgNwClGarp.disabled
        current.cluster_master_election_priority = 0
        current.gateway_tracking_state = EnumHaSwitchNewCfgTrigGwTrackState.disabled
        current.real_server_tracking_state = EnumHaSwitchNewCfgTriggerl4Reals.disabled
        current.unicast_session_mirroring = EnumSlbNewCfgSyncUcastSfo.disabled
        current.sync_persistent_sessions = EnumSlbNewCfgSyncSfo.disabled
        current.sync_dynamic_data_store = EnumSlbNewCfgSyncDynamicData.disabled
        current.mirroring_primary_interface = 0
        current.mirroring_secondary_interface = 0
        current.sync_session_interval_seconds = 30
        self.update(current, dry_run=dry_run)
        self._update_ha_state(EnumHaNewCfgMode.disabled, dry_run=dry_run)
        return 'HA configuration' + MSG_DELETE

    def _update_remove(self, parameters: HighAvailabilityParameters, dry_run: bool) -> str:
        current = self._read(HighAvailabilityParameters())
        if current.mode != EnumHaNewCfgMode.switch:
            self._update_ha_state(EnumHaNewCfgMode.switch, dry_run=dry_run)
        self._update_advertise_track_objects(parameters.advertising_interfaces, 'haSwitchNewCfgRemIf', dry_run)
        self._update_advertise_track_objects(parameters.tracked_interfaces, 'haSwitchNewCfgTrigIfTrackExclude', dry_run)
        self._update_advertise_track_objects(parameters.tracked_gateways, 'haSwitchNewCfgTrigGwTrackExclude', dry_run)
        self._update_ha_state(current.mode, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def _update_ha_state(self, state, dry_run):
        root = Root()
        root.haNewCfgMode = state
        self._device_api.update(root, dry_run=dry_run)

    def _update_advertise_track_objects(self, obj_id_list, root_attr_name, dry_run):
        if obj_id_list is not None:
            for oid in obj_id_list:
                root = Root()
                setattr(root, root_attr_name, oid)
                self._device_api.update(root, dry_run=dry_run)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            mode='disabled',
            preferred_state='standby',
            advertising_interfaces=None,
            tracked_interfaces=None,
            tracked_gateways=None,
            fail_back_mode='onfailure',
            holdoff_timer_second=0,
            advertisement_interval_second=1,
            advertise_bgp_routes_on_backup='disabled',
            send_garp_nwclss_proxy_ips='disabled',
            cluster_master_election_priority=0,
            gateway_tracking_state='disabled',
            real_server_tracking_state='disabled',
            unicast_session_mirroring='disabled',
            sync_persistent_sessions='disabled',
            sync_dynamic_data_store='disabled',
            mirroring_primary_interface=0,
            mirroring_secondary_interface=0,
            sync_session_interval_seconds=30
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure

