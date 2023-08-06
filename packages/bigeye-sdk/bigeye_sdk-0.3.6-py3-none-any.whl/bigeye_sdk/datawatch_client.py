from __future__ import annotations

import abc
import enum
import json
from typing import List, Optional, Union

import requests
from requests.auth import HTTPBasicAuth

from bigeye_sdk.functions.delta_functions import infer_column_mappings
from bigeye_sdk.functions.metric_functions import is_same_metric, is_same_column_metric, \
    set_default_model_type_for_threshold
from bigeye_sdk.functions.urlfuncts import encode_url_params

from bigeye_sdk.generated.com.torodata.models.generated import TableList, ColumnMetricProfileList, \
    AutometricAcceptRequest, \
    AutometricAcceptResponse, GetMetricInfoListRequest, MetricInfoList, SearchMetricConfigurationRequest, \
    BatchGetMetricResponse, MetricCreationState, ThreeLeggedBoolean, MetricSortField, SortDirection, \
    MetricConfiguration, TimeInterval, Threshold, MetricType, MetricParameter, LookbackType, NotificationChannel, \
    MetricBackfillResponse, MetricBackfillRequest, GetCollectionsResponse, GetCollectionResponse, Collection, \
    EditCollectionResponse, EditCollectionRequest, \
    GetDeltaApplicableMetricTypesResponse, CreateComparisonTableResponse, CreateComparisonTableRequest, \
    ComparisonTableConfiguration, IdAndDisplayName, ComparisonColumnMapping, \
    ColumnNamePair, BatchRunMetricsRequest, BatchRunMetricsResponse, \
    GetSourceListResponse, Empty, Source, CreateSourceRequest, BatchMetricConfigRequest, \
    BatchMetricConfigResponse, Table, ComparisonTableInfo, GetComparisonTableInfosResponse, RunComparisonTableResponse, \
    GetComparisonTableInfosRequest

# create logger
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.api_credentials import BasicAuthRequestLibApiConf

log = get_logger(__file__)


class Method(str, enum.Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'

    def __str__(self):
        return self.name


class DatawatchClient(abc.ABC):

    @abc.abstractmethod
    def _call_datawatch(self, method: Method, url, body: str = None):
        pass

    def get_dataset(self, warehouse_id: int, schema_name: str) -> List[dict]:
        """
        Provides advanced dataset details for a schema but returns a list of dictionaries instead of an list of Table
        objects.

        Args:
            warehouse_id:
            schema_name:

        Returns: list of dictionaries containing advanced details about all datasets in a schema.

        """
        url = f"/dataset/tables/{warehouse_id}/{schema_name}"

        return self._call_datawatch(Method.GET, url)

    def get_tables(self,
                   *,
                   warehouse_id: List[int] = [],
                   schema: List[str] = [],
                   table_name: List[str] = [],
                   ids: List[int] = [],
                   schema_id: List[int] = []) -> TableList:
        url = f"/api/v1/tables?{encode_url_params(locals(), remove_keys=['api_conf'])}"
        log.info('Getting warehouse tables.')
        log.info(url)
        response = self._call_datawatch(Method.GET, url)
        tables = TableList().from_dict(response)
        return tables

    def get_table_ids(self,
                      warehouse_id: List[int] = [],
                      schemas: List[str] = [],
                      table_name: List[str] = [],
                      ids: List[int] = [],
                      schema_id: List[int] = []) -> List[int]:
        return [t.id for t in self.get_tables(warehouse_id=warehouse_id, schema=schemas, table_name=table_name,
                                              ids=ids, schema_id=schema_id).tables]

    def rebuild(self, warehouse_id: int, schema_name: str = None):
        """
        TODO: switch to returning an object from the protobuf.

        Args:
            warehouse_id:
            schema_name:

        Returns: list of metrics.

        """
        url = f'/dataset/rebuild/{warehouse_id}'

        if schema_name is not None:
            url = url + f'/{schema_name}'

        return self._call_datawatch(Method.GET, url)

    def get_table_profile(self, table_id: int) -> ColumnMetricProfileList:
        url = f'/api/v1/tables/profile/{table_id}'
        return ColumnMetricProfileList().from_dict(self._call_datawatch(Method.GET, url))

    def batch_delete_metrics(self, metric_ids: List[int]):
        body = json.dumps({"metricIds": metric_ids})
        log.info(f'Deleting metrics: {metric_ids}')
        url = f'/statistics'
        return self._call_datawatch(Method.DELETE, url, body)

    def accept_autometrics(
            self, *, metric_ids: List[int] = [], lookback_days: int = 7
    ) -> AutometricAcceptResponse:
        """Batch accept autometrics"""

        request = AutometricAcceptRequest()
        request.metric_ids = metric_ids
        request.lookback_days = lookback_days

        url = f'/api/v1/metrics/autometrics/accept'
        body = request.to_json()
        log.info(f'Deploying autometrics: {url} -- {body}')
        r = self._call_datawatch(Method.POST, url, body)
        return AutometricAcceptResponse().from_dict(r)

    def search_metric_configuration(
            self,
            *,
            ids: List[int] = [],
            warehouse_ids: List[int] = [],
            table_ids: List[int] = [],
            table_name: str = "",
            status: str = "",
            muted: bool = False,
    ) -> BatchGetMetricResponse:
        """Search metric configurations"""

        request = SearchMetricConfigurationRequest()
        request.ids = ids
        request.warehouse_ids = warehouse_ids
        request.table_ids = table_ids
        request.table_name = table_name
        request.status = status
        request.muted = muted

        url = f'/api/v1/metrics?{encode_url_params(d=request.to_dict())}'

        response = self._call_datawatch(Method.GET, url=url)

        return BatchGetMetricResponse().from_dict(response)

    # TODO Deprecated
    def get_metric_info_batch_post_dict(
            self,
            *,
            metric_ids: List[int] = [],
            warehouse_ids: List[int] = [],
            table_ids: List[int] = [],
            table_name: str = "",
            status: str = "",
            metric_creation_states: List[MetricCreationState] = [],
            muted: ThreeLeggedBoolean = 0,
            page_size: int = 0,
            page_cursor: str = "",
            sort_field: MetricSortField = 0,
            schema_name: str = "",
            column_ids: List[int] = [],
            search: str = "",
            sort_direction: SortDirection = 0,
    ) -> dict:
        """Get batch metric information"""

        request = GetMetricInfoListRequest()
        request.metric_ids = metric_ids
        request.warehouse_ids = warehouse_ids
        request.table_ids = table_ids
        request.table_name = table_name
        request.status = status
        request.metric_creation_states = metric_creation_states
        request.muted = muted
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.schema_name = schema_name
        request.column_ids = column_ids
        request.search = search
        request.sort_direction = sort_direction

        url = '/api/v1/metrics/info'

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        mil_current = MetricInfoList().from_dict(response)
        mil_return = MetricInfoList()

        while mil_current.pagination_info.next_cursor:
            mil_return.metrics.extend(mil_current.metrics)
            request.page_cursor = mil_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
            mil_current = MetricInfoList().from_dict(response)

        return response['metrics']

    def get_metric_info_batch_post(
            self,
            *,
            metric_ids: List[int] = [],
            warehouse_ids: List[int] = [],
            table_ids: List[int] = [],
            table_name: str = "",
            status: str = "",
            metric_creation_states: List[MetricCreationState] = [],
            muted: ThreeLeggedBoolean = 0,
            page_size: int = 0,
            page_cursor: str = "",
            sort_field: MetricSortField = 0,
            schema_name: str = "",
            column_ids: List[int] = [],
            search: str = "",
            sort_direction: SortDirection = 0,
    ) -> MetricInfoList:
        """Get batch metric information"""

        request = GetMetricInfoListRequest()
        request.metric_ids = metric_ids
        request.warehouse_ids = warehouse_ids
        request.table_ids = table_ids
        request.table_name = table_name
        request.status = status
        request.metric_creation_states = metric_creation_states
        request.muted = muted
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.schema_name = schema_name
        request.column_ids = column_ids
        request.search = search
        request.sort_direction = sort_direction

        url = '/api/v1/metrics/info'

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        mil_current = MetricInfoList().from_dict(response)
        mil_return = MetricInfoList()

        while mil_current.pagination_info.next_cursor:
            mil_return.metrics.extend(mil_current.metrics)
            request.page_cursor = mil_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
            mil_current = MetricInfoList().from_dict(response)

        return MetricInfoList().from_dict(response)

    def get_existing_metric(self,
                            warehouse_id: int, table: Table, column_name: str,
                            metric_name: str, group_by: List[str], filters: List[str]):
        """
        Get an existing metric by name and group_by.
        TODO: Must add user defined name because we are assuming multiple Averages on the same column.  Could be different conditions.
        """
        metrics = self.search_metric_configuration(warehouse_ids=[warehouse_id], table_ids=[table.id])

        for m in metrics.metrics:
            if is_same_metric(m, metric_name, group_by, filters) \
                    and is_same_column_metric(m, column_name):
                return m
        return None

    def create_metric(
            self,
            *,
            id: int = 0,
            schedule_frequency: Optional[TimeInterval] = None,
            filters: List[str] = [],
            group_bys: List[str] = [],
            thresholds: List[Threshold] = [],
            notification_channels: List[NotificationChannel] = [],
            warehouse_id: int = 0,
            dataset_id: int = 0,
            metric_type: Optional[MetricType] = None,
            parameters: List[MetricParameter] = [],
            lookback: Optional[TimeInterval] = None,
            lookback_type: LookbackType = 0,
            metric_creation_state: MetricCreationState = 0,
            grain_seconds: int = 0,
            muted_until_epoch_seconds: int = 0,
            name: str = "",
            description: str = "",
            metric_configuration: MetricConfiguration = None
    ) -> MetricConfiguration:
        """Create or update metric"""

        if metric_configuration:
            request = metric_configuration
        else:
            request = MetricConfiguration()
            request.id = id
            if schedule_frequency is not None:
                request.schedule_frequency = schedule_frequency
            request.filters = filters
            request.group_bys = group_bys
            if thresholds is not None:
                request.thresholds = set_default_model_type_for_threshold(thresholds)
            if notification_channels is not None:
                request.notification_channels = notification_channels
            request.warehouse_id = warehouse_id
            request.dataset_id = dataset_id
            if metric_type is not None:
                request.metric_type = metric_type
            if parameters is not None:
                request.parameters = parameters
            if lookback is not None:
                request.lookback = lookback
            request.lookback_type = lookback_type
            request.metric_creation_state = metric_creation_state
            request.grain_seconds = grain_seconds
            request.muted_until_epoch_seconds = muted_until_epoch_seconds
            request.name = name
            request.description = description

        set_default_model_type_for_threshold(request.thresholds)

        url = "/api/v1/metrics"

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return MetricConfiguration().from_dict(response)

    def backfill_autothresholds(self,
                                metric_ids: List[int] = []):
        for metric_id in metric_ids:
            log.info(f"Backfilling autothreshold: {metric_id}")
            url = f"/statistics/backfillAutoThresholds/{metric_id}"
            response = self._call_datawatch(Method.GET, url=url)

    def backfill_metric(
            self,
            *,
            metric_ids: List[int] = [],
            backfill_range: Optional["TimeRange"] = None,
    ) -> MetricBackfillResponse:
        """Backfill metric"""

        request = MetricBackfillRequest()
        request.metric_ids = metric_ids
        if backfill_range is not None:
            request.backfill_range = backfill_range

        url = "/api/v1/metrics/backfill"

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return MetricBackfillResponse().from_dict(response)

    def regen_autometrics(self, table_id: int):
        url = f'/statistics/suggestions/{table_id}'
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)

    def get_collections(self) -> GetCollectionsResponse:
        url = "/api/v1/collections/"
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)
        return GetCollectionsResponse().from_dict(response)

    def get_collection(self, collection_id: int) -> GetCollectionResponse:
        url = f"/api/v1/collections/{collection_id}"
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)
        return GetCollectionResponse().from_dict(response)

    def create_collection(self, collection: Collection) -> EditCollectionResponse:
        url = f"/api/v1/collections"

        request: EditCollectionRequest = EditCollectionRequest()
        request.collection_name = collection.name
        request.description = collection.description
        request.metric_ids = collection.metric_ids
        request.notification_channels = collection.notification_channels
        request.muted_until_timestamp = collection.muted_until_timestamp

        log.info(f'Query: {url}; Body: {request.to_json()}')

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return EditCollectionResponse().from_dict(response)

    def update_collection(self, collection: Collection) -> EditCollectionResponse:
        url = f"/api/v1/collections"

        request: EditCollectionRequest = EditCollectionRequest()
        request.collection_name = collection.name
        request.description = collection.description
        request.metric_ids = collection.metric_ids
        request.notification_channels = collection.notification_channels
        request.muted_until_timestamp = collection.muted_until_timestamp

        log.info(f'Query: {url}; Body: {request.to_json()}')

        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())

        return EditCollectionResponse().from_dict(response)

    def upsert_metric_to_collection(self, collection_id: int,
                                    add_metric_ids: Union[int, List[int]]) -> EditCollectionResponse:

        if type(add_metric_ids) == int:
            mids = list(add_metric_ids)
        else:
            mids = add_metric_ids

        collection: Collection = self.get_collection(collection_id=collection_id).collection

        for mid in mids:
            collection.metric_ids.append(mid)

        return self.update_collection(collection=collection)

    def get_delta_applicable_metric_types(
            self, *, table_id: int = 0
    ) -> GetDeltaApplicableMetricTypesResponse:
        """
        Get list of metrics applicable for deltas
        Args:
            table_id: source table id

        Returns: list of metrics applicable for deltas.

        """

        url = f"/api/v1/tables/{table_id}/delta-applicable-metric-types"

        response = self._call_datawatch(Method.GET, url)

        return GetDeltaApplicableMetricTypesResponse().from_dict(response)

    def create_delta(
            self,
            name: str,
            source_table_id: int,
            target_table_id: int,
            column_mappings: List[ComparisonColumnMapping] = [],
            named_schedule: IdAndDisplayName = None,
            group_bys: List[ColumnNamePair] = [],
            source_filters: List[str] = [],
            target_filters: List[str] = [],
            comparison_table_configuration: Optional["ComparisonTableConfiguration"] = None,
    ) -> CreateComparisonTableResponse:
        """

        Args:
            name: Required.  Name of delta
            source_table_id:  Required.  table id for source table
            target_table_id: Required. Table id for target table
            column_mappings: Optional. If not exists then will infer from applicable table mappings based on column name.
            named_schedule: Optional.  No schecule if not exists
            group_bys: Optional.  No group bys if not exists
            source_filters: Optional.  No filters if not exists
            target_filters: Optional.  No filters if not exists
            comparison_table_configuration: Optional.

        Returns:  CreateComparisonTableResponse

        """

        if not column_mappings:
            source_metric_types = self.get_delta_applicable_metric_types(table_id=source_table_id).metric_types
            target_metric_types = self.get_delta_applicable_metric_types(table_id=target_table_id).metric_types
            column_mappings = infer_column_mappings(source_metric_types=source_metric_types,
                                                    target_metric_types=target_metric_types)

        url = '/api/v1/metrics/comparisons/tables'

        request = CreateComparisonTableRequest()
        if comparison_table_configuration is not None:
            request.comparison_table_configuration = comparison_table_configuration
        else:
            request.comparison_table_configuration.name = name
            request.comparison_table_configuration.source_table_id = source_table_id
            request.comparison_table_configuration.target_table_id = target_table_id
            request.comparison_table_configuration.column_mappings = column_mappings
            if named_schedule:
                request.comparison_table_configuration.named_schedule = named_schedule
            request.comparison_table_configuration.group_bys = group_bys
            request.comparison_table_configuration.source_filters = source_filters
            request.comparison_table_configuration.target_filters = target_filters
            request.comparison_table_configuration.target_table_id = target_table_id

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return CreateComparisonTableResponse().from_dict(response)

    def run_a_delta(self, *, delta_id: int) -> ComparisonTableInfo:

        url = f"/api/v1/metrics/comparisons/tables/run/{delta_id}"
        response = self._call_datawatch(Method.GET, url)

        return RunComparisonTableResponse().from_dict(response).comparison_table_info

    def get_delta_information(self, *, delta_ids: List[int],
                              exclude_comparison_metrics: bool = False) -> List[ComparisonTableInfo]:

        url = "/api/v1/metrics/comparisons/tables/info"
        request = GetComparisonTableInfosRequest(delta_ids, exclude_comparison_metrics)
        response = self._call_datawatch(Method.POST, url, request.to_json())

        return GetComparisonTableInfosResponse().from_dict(response).comparison_table_infos

    def run_metric_batch(
            self, *, metric_ids: List[int] = []
    ) -> BatchRunMetricsResponse:
        """Batch run metrics"""

        request = BatchRunMetricsRequest()
        request.metric_ids = metric_ids

        url = '/api/v1/metrics/run/batch'

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return BatchRunMetricsResponse().from_dict(response)

    def get_sources(self) -> GetSourceListResponse:
        """Get sources"""
        url = "/api/v1/sources/fetch"
        request = Empty()

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return GetSourceListResponse().from_dict(response)

    def edit_metric(self, metric_configuration: MetricConfiguration = None) -> BatchMetricConfigResponse:
        """
        TODO: Only supporting 1 metric because of weird defaults and required fields.
        Args:
            metric_configuration:

        Returns:

        """
        url = "/api/v1/metrics/batch"

        request = BatchMetricConfigRequest()
        request.metric_ids = [metric_configuration.id]

        request.metric_configuration = metric_configuration
        request_json = request.to_json()

        response = self._call_datawatch(Method.PUT, url, request_json)

        return BatchMetricConfigResponse().from_dict(response)

    def create_source(self, request: CreateSourceRequest) -> Source:

        url = 'api/v1/sources'

        response = self._call_datawatch(Method.POST, url, request.to_json())
        source = Source().from_dict(value=response.json()['source'])
        log.info(f'Source {source.name} created with warehouse ID: {source.id}')
        return source

    def delete_metric(self, *, metric_id: int):
        """Delete metric"""

        url = f'/api/v1/metrics/{metric_id}'

        self._call_datawatch(Method.DELETE, url)

    def delete_source(self, warehouse_id: int):

        url = f'/api/v1/sources/{warehouse_id}'

        self._call_datawatch(Method.DELETE, url)
        log.info(f'Begin delete for warehouse ID: {warehouse_id}')


class CoreDatawatchClient(DatawatchClient):
    def __init__(self, api_conf: BasicAuthRequestLibApiConf):
        self._base_url = api_conf.base_url
        self._auth = HTTPBasicAuth(api_conf.user, api_conf.password)
        pass

    def _call_datawatch(self, method: Method, url, body: str = None):
        try:
            fq_url = f'{self._base_url}{url}'
            log.info(f'Request Type: {method.name}; URL: {fq_url}; Body: {body}')
            if method == Method.GET:
                response = requests.get(
                    fq_url,
                    auth=self._auth
                )
            elif method == Method.POST:
                response = requests.post(
                    fq_url,
                    headers={"Content-Type": "application/json", "Accept": "application/json"},
                    data=body,
                    auth=self._auth
                )
            elif method == Method.PUT:
                response = requests.put(
                    fq_url,
                    headers={"Content-Type": "application/json", "Accept": "application/json"},
                    data=body,
                    auth=self._auth
                )
            elif method == Method.DELETE:
                response = requests.delete(f'{self._base_url}{url}',
                                           headers={"Content-Type": "application/json", "Accept": "application/json"},
                                           data=body,
                                           auth=self._auth)
            else:
                raise Exception(f'Unsupported http method {method}')
        except Exception as e:
            log.error(f'Exception calling datawatch: {str(e)}')
            raise e
        else:
            log.info(f'Return Code: {response.status_code}')
            if response.status_code < 200 or response.status_code >= 300:
                log.error(f'Error code returned from datawatch: {str(response)}')
                raise Exception(response.text)
            else:
                # Not empty response
                if response.status_code != 204:
                    return response.json()
