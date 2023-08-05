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
from radware.alteon.beans.GslbNewCfgRuleTable import *
from radware.alteon.beans.GslbNewCfgMetricTable import *
from radware.sdk.configurator import DryRunDeleteProcedure
from typing import List, Optional, ClassVar


class GSLBRuleMetricEntry(RadwareParametersStruct):
    priority: int
    metric: EnumGslbMetricMetric
    network_ids: Optional[List[int]]

    def __init__(self, priority: int = None, metric: EnumGslbMetricMetric = None):
        self.priority = priority
        self.metric = metric
        self.network_ids = list()

    def struct_normalization(self):
        if self.network_ids is not None and type(self.network_ids) == str:
            self.network_ids = BeanUtils.decode_bmp(self.network_ids)


class GSLBRuleParameters(RadwareParametersStruct):
    index: int
    state: Optional[EnumGslbRuleState]
    dns_ttl: Optional[int]
    max_dns_resource_records: Optional[int]
    domain_name: Optional[str]
    src_dns_persist_mask: Optional[str]
    dns_persist_timeout: Optional[int]
    src6_dns_persist_prefix: Optional[int]
    rule_type: Optional[EnumGslbRuleType]
    description: Optional[str]
    edns_persist_mode: Optional[EnumGslbRuleEdnsPrst]
    rule_network_fallback: Optional[EnumGslbRuleNetworkFallback]
    rule_metrics: Optional[List[GSLBRuleMetricEntry]]

    def __init__(self, index: int = None):
        self.index = index
        self.state = None
        self.dns_ttl = None
        self.max_dns_resource_records = None
        self.domain_name = None
        self.src_dns_persist_mask = None
        self.dns_persist_timeout = None
        self.src6_dns_persist_prefix = None
        self.rule_type = None
        self.description = None
        self.edns_persist_mode = None
        self.rule_network_fallback = None
        self.rule_metrics = list()


bean_map = {
    GslbNewCfgRuleTable: dict(
        struct=GSLBRuleParameters,
        direct=True,
        attrs=dict(
            Indx='index',
            State='state',
            TTL='dns_ttl',
            RR='max_dns_resource_records',
            Dname='domain_name',
            IpNetMask='src_dns_persist_mask',
            Timeout='dns_persist_timeout',
            Ipv6Prefix='src6_dns_persist_prefix',
            Type='rule_type',
            Name='description',
            EdnsPrst='edns_persist_mode',
            NetworkFallback='rule_network_fallback'
        )
    ),
    GslbNewCfgMetricTable: dict(
        struct=List[GSLBRuleMetricEntry],
        direct=True,
        attrs=dict(
            RuleMetricIndx='index',
            Indx='priority',
            Metric='metric',
            NetworkBmap='network_ids'

        )
    )
}


class GSLBRuleConfigurator(AlteonConfigurator, NumericConfigurator):
    parameters_class: ClassVar[GSLBRuleParameters]

    def __init__(self, alteon_connection):
        AlteonConfigurator.__init__(self, bean_map, alteon_connection)

    def _read(self, parameters: GSLBRuleParameters) -> GSLBRuleParameters:
        self._read_device_beans(parameters)
        if self._beans:
            for metric in parameters.rule_metrics:
                metric.network_ids = BeanUtils.decode_bmp(metric.network_ids)
            return parameters

    def _update(self, parameters: GSLBRuleParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=[GslbNewCfgMetricTable])
        if parameters.rule_metrics:
            for metric in parameters.rule_metrics:
                metric_entry = self._get_bean_instance(GslbNewCfgMetricTable, metric)
                metric_entry.RuleMetricIndx = parameters.index
                metric_entry.Metric = metric.metric
                self._device_api.update(metric_entry, dry_run=dry_run)
                if metric.network_ids:
                    for net in metric.network_ids:
                        metric_entry.AddNetwork = net
                        self._device_api.update(metric_entry, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: GSLBRuleParameters, dry_run: bool) -> str:
        if parameters.rule_metrics:
            for metric in parameters.rule_metrics:
                metric_entry = self._get_bean_instance(GslbNewCfgMetricTable, metric)
                metric_entry.RuleMetricIndx = parameters.index
                metric_entry.Metric = EnumGslbMetricMetric.none
                self._device_api.update(metric_entry, dry_run=dry_run)
                if metric.network_ids:
                    for net in metric.network_ids:
                        metric_entry.RemNetwork = net
                        self._device_api.update(metric_entry, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(GslbNewCfgRuleTable, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        metrics = list()
        if 'rule_metrics' in diff:
            for item in diff['rule_metrics']:
                if item['metric'] != 'none' or item['network_ids']:
                    metrics.append(item)
            if metrics:
                diff['rule_metrics'] = metrics
            else:
                diff.pop('rule_metrics')
        return dry_run_procedure

