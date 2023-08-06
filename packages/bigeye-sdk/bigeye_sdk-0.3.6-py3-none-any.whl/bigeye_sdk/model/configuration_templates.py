from __future__ import annotations

import yaml
import inspect
from dataclasses import dataclass, field
from typing import List, Optional

from smart_open import smart_open

from bigeye_sdk.decorators.dataclass_decorators import add_from_dict
from bigeye_sdk.log import get_logger

# create logger
from bigeye_sdk.model.enums import SimpleMetricType
from bigeye_sdk.functions.metric_functions import get_notification_channels, get_thresholds_for_metric, \
    get_freshness_metric_name_for_field, is_freshness_metric, enforce_lookback_type_defaults, \
    get_seconds_from_window_size, table_has_metric_time, get_lookback_type, get_grain_seconds, \
    merge_existing_metric_conf
from bigeye_sdk.generated.com.torodata.models.generated import TimeIntervalType, TimeInterval, MetricParameter, \
    MetricConfiguration, Threshold, Table, MetricType

log = get_logger(__file__)


@dataclass
class SimpleUpsertMetricRequest:
    schema_name: str
    table_name: str
    column_name: str
    metric_template: SimpleMetricTemplate = None
    from_metric: int = None

    def build_upsert_request_object(self, target_table: Table):
        return self.metric_template.build_upsert_request_object(target_table=target_table,
                                                                column_name=self.column_name,
                                                                existing_metric=None)

    @classmethod
    def from_dict(cls, d: dict) -> SimpleUpsertMetricRequest:
        [cls_params, smt_params] = map(lambda keys: {x: d[x] for x in keys if x in d},
                                       [inspect.signature(cls).parameters,
                                        inspect.signature(SimpleMetricTemplate).parameters])

        cls_params["metric_template"] = SimpleMetricTemplate.from_dict(smt_params) if smt_params \
            else SimpleMetricTemplate.from_dict(cls_params["metric_template"])
        return cls(**cls_params)


@dataclass
@add_from_dict
class SimpleMetricTemplate:
    """
    Provides a simple, string based metric template for interacting with the Bigeye API.
    """
    metric_name: str  # system metric name (name of the predefined metric or the name of the template)
    user_defined_metric_name: str = None  # user defined name of metric.  Defaults to system metric name.
    metric_type: SimpleMetricType = SimpleMetricType.PREDEFINED  # the actual metric type
    notifications: List[str] = field(default_factory=lambda: [])
    thresholds: List[Threshold] = field(default_factory=lambda: [])
    filters: List[str] = field(default_factory=lambda: [])
    group_by: List[str] = field(default_factory=lambda: [])
    default_check_frequency_hours: int = 2
    update_schedule: str = None  # cron schedule.
    delay_at_update: str = "0 minutes"
    timezone: str = "UTC"
    should_backfill: bool = False
    lookback_type: str = None
    lookback_days: int = 2
    window_size: str = "1 day"
    window_size_seconds = get_seconds_from_window_size(window_size)

    def __post_init__(self):
        if self.user_defined_metric_name is None:
            # Default the user_defined_metric_name to the system metric name.
            self.user_defined_metric_name = self.metric_name

        self.lookback_type = enforce_lookback_type_defaults(predefined_metric_name=self.metric_name,
                                                            lookback_type=self.lookback_type)

    def build_upsert_request_object(self,
                                    target_table: Table,
                                    column_name: str,
                                    existing_metric: MetricConfiguration = None) -> MetricConfiguration:
        """
        Converts a SimpleMetricTemplate to a MetricConfiguration that can be used to upsert a metric to Bigeye API.
        Must include either a column name or an existing metric

        TODO: Break out any remaining logic and unit test.  Currently the table dict makes this harder to test.

        :param target_table: The table object to which the metric will be deployed
        :param column_name: The column name to which the metric will be deployed.
        :param existing_metric: (Optional) Pass the existing MetricConfiguration if updating
        :return:
        """

        new_metric = MetricConfiguration()
        new_metric.name = self.user_defined_metric_name
        new_metric.schedule_frequency = TimeInterval(
            interval_type=TimeIntervalType.HOURS_TIME_INTERVAL_TYPE,
            interval_value=self.default_check_frequency_hours
        )

        new_metric.thresholds = get_thresholds_for_metric(self.metric_name, self.timezone, self.delay_at_update,
                                                          self.update_schedule, self.thresholds)

        new_metric.warehouse_id = target_table.warehouse_id

        new_metric.dataset_id = target_table.id

        metric_time_exists = table_has_metric_time(target_table)

        ifm = is_freshness_metric(self.metric_name)

        new_metric.metric_type = self._set_new_metric_type(ifm, target_table, column_name)

        new_metric.parameters = [MetricParameter(key="arg1", column_name=column_name)]

        new_metric.lookback = TimeInterval(interval_type=TimeIntervalType.DAYS_TIME_INTERVAL_TYPE,
                                           interval_value=self.lookback_days)

        new_metric.notification_channels = get_notification_channels(self.notifications)

        new_metric.filters = self.filters

        new_metric.group_bys = self.group_by

        new_metric.lookback_type = get_lookback_type(lookback_type=self.lookback_type,
                                                     metric_time_exists=metric_time_exists)

        new_metric.grain_seconds = get_grain_seconds(lookback_type=new_metric.lookback_type,
                                                     window_size_seconds=self.window_size_seconds)

        return merge_existing_metric_conf(new_metric=new_metric, is_freshness_metric=ifm,
                                          metric_time_exists=metric_time_exists, existing_metric=existing_metric)

    def _set_new_metric_type(self,
                             freshness_metric: bool,
                             target_table: Table,
                             column_name: str) -> MetricType:

        if freshness_metric:
            # Enforce correct metric name for field type.
            new_metric_type = get_freshness_metric_name_for_field(target_table, column_name)
            if self.update_schedule is None:
                raise Exception("Update schedule can not be null for freshness schedule thresholds")
        else:
            new_metric_type = self.metric_type.factory(self.metric_name)

        return new_metric_type


@dataclass
class DeltaCICDConf:
    delta_name_prefix: str
    source_warehouse_id: int
    source_fqtn: str
    target_warehouse_id: int
    target_fqtn: str
    report_model_fqcn: str
    second_pass_group_bys: Optional[List[str]]

    @classmethod
    def load_conf(cls, delta_conf_file: str):
        with smart_open(delta_conf_file, 'r') as stream:
            conf = yaml.safe_load(stream)
            dc = DeltaCICDConf(**conf)
            if dc is None:
                raise Exception('Could not load delta configuration file.')
            return dc


