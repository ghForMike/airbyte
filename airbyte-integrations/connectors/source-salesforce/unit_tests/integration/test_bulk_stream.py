# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

import json
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from unittest import TestCase

import freezegun
from airbyte_cdk.sources.source import TState
from airbyte_cdk.test.catalog_builder import CatalogBuilder
from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput, read
from airbyte_cdk.test.mock_http import HttpMocker, HttpRequest, HttpResponse
from airbyte_cdk.test.mock_http.request import ANY_QUERY_PARAMS
from airbyte_cdk.test.state_builder import StateBuilder
from airbyte_protocol.models import ConfiguredAirbyteCatalog, SyncMode
from config_builder import ConfigBuilder
from integration.utils import given_stream
from salesforce_describe_response_builder import SalesforceDescribeResponseBuilder
from source_salesforce import SourceSalesforce
from source_salesforce.streams import LOOKBACK_SECONDS

_A_FIELD_NAME = "a_field"
_ACCESS_TOKEN = "an_access_token"
_API_VERSION = "v57.0"
_CLIENT_ID = "a_client_id"
_CLIENT_SECRET = "a_client_secret"
_CURSOR_FIELD = "SystemModstamp"
_INSTANCE_URL = "https://instance.salesforce.com"
_JOB_ID = "a-job-id"
_LOOKBACK_WINDOW = timedelta(seconds=LOOKBACK_SECONDS)
_NOW = datetime.now(timezone.utc)
_REFRESH_TOKEN = "a_refresh_token"
_STREAM_NAME = "a_stream_name"

_BASE_URL = f"{_INSTANCE_URL}/services/data/{_API_VERSION}"


def _catalog(sync_mode: SyncMode) -> ConfiguredAirbyteCatalog:
    return CatalogBuilder().with_stream(_STREAM_NAME, sync_mode).build()


def _source(catalog: ConfiguredAirbyteCatalog, config: Dict[str, Any], state: Optional[TState]) -> SourceSalesforce:
    return SourceSalesforce(catalog, config, state)


def _read(
    sync_mode: SyncMode,
    config_builder: Optional[ConfigBuilder] = None,
    state_builder: Optional[StateBuilder] = None,
    expecting_exception: bool = False
) -> EntrypointOutput:
    catalog = _catalog(sync_mode)
    config = config_builder.build() if config_builder else ConfigBuilder().build()
    state = state_builder.build() if state_builder else StateBuilder().build()
    return read(_source(catalog, config, state), config, catalog, state, expecting_exception)


def _given_authentication(http_mocker: HttpMocker, client_id: str, client_secret: str, refresh_token: str) -> None:
    http_mocker.post(
        HttpRequest(
            "https://login.salesforce.com/services/oauth2/token",
            query_params=ANY_QUERY_PARAMS,
            body=f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"
        ),
        HttpResponse(json.dumps({"access_token": _ACCESS_TOKEN, "instance_url": _INSTANCE_URL})),
    )


def _create_field(name: str, _type: Optional[str] = None) -> Dict[str, Any]:
    return {"name": name, "type": _type if _type else "string"}


def _to_url(to_convert: datetime) -> str:
    to_format = to_convert.isoformat(timespec="milliseconds")
    return urllib.parse.quote_plus(to_format)


def _to_partitioned_datetime(to_convert: datetime) -> str:
    return to_convert.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _calculate_start_time(start_time: datetime) -> datetime:
    # the start is granular to the second hence why we have `0` in terms of milliseconds
    return start_time.replace(microsecond=0)


@freezegun.freeze_time(_NOW.isoformat())
class FullRefreshTest(TestCase):

    def setUp(self) -> None:
        self._config = ConfigBuilder().client_id(_CLIENT_ID).client_secret(_CLIENT_SECRET).refresh_token(_REFRESH_TOKEN)

    @HttpMocker()
    def test_when_read_then_create_job_and_extract_records_from_result(self, http_mocker: HttpMocker) -> None:
        _given_authentication(http_mocker, _CLIENT_ID, _CLIENT_SECRET, _REFRESH_TOKEN)
        given_stream(http_mocker, _BASE_URL, _STREAM_NAME, SalesforceDescribeResponseBuilder().field(_A_FIELD_NAME))
        http_mocker.post(
            HttpRequest(f"{_BASE_URL}/jobs/query", body=json.dumps({"operation": "queryAll", "query": "SELECT a_field FROM a_stream_name", "contentType": "CSV", "columnDelimiter": "COMMA", "lineEnding": "LF"})),
            HttpResponse(json.dumps({"id": _JOB_ID})),
        )
        http_mocker.get(
            HttpRequest(f"{_BASE_URL}/jobs/query/{_JOB_ID}"),
            HttpResponse(json.dumps({"state": "JobComplete"})),
        )
        http_mocker.get(
            HttpRequest(f"{_BASE_URL}/jobs/query/{_JOB_ID}/results"),
            HttpResponse(f"{_A_FIELD_NAME}\nfield_value"),
        )

        output = _read(SyncMode.full_refresh, self._config)

        assert len(output.records) == 1
