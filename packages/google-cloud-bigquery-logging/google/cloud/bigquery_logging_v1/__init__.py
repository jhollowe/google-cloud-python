# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.cloud.bigquery_logging_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .types.audit_data import (
    AuditData,
    BigQueryAcl,
    Dataset,
    DatasetInfo,
    DatasetInsertRequest,
    DatasetInsertResponse,
    DatasetListRequest,
    DatasetName,
    DatasetUpdateRequest,
    DatasetUpdateResponse,
    EncryptionInfo,
    Job,
    JobCompletedEvent,
    JobConfiguration,
    JobGetQueryResultsRequest,
    JobGetQueryResultsResponse,
    JobInsertRequest,
    JobInsertResponse,
    JobName,
    JobQueryDoneResponse,
    JobQueryRequest,
    JobQueryResponse,
    JobStatistics,
    JobStatus,
    Table,
    TableDataListRequest,
    TableDataReadEvent,
    TableDefinition,
    TableInfo,
    TableInsertRequest,
    TableInsertResponse,
    TableName,
    TableUpdateRequest,
    TableUpdateResponse,
    TableViewDefinition,
)

__all__ = (
    "AuditData",
    "BigQueryAcl",
    "Dataset",
    "DatasetInfo",
    "DatasetInsertRequest",
    "DatasetInsertResponse",
    "DatasetListRequest",
    "DatasetName",
    "DatasetUpdateRequest",
    "DatasetUpdateResponse",
    "EncryptionInfo",
    "Job",
    "JobCompletedEvent",
    "JobConfiguration",
    "JobGetQueryResultsRequest",
    "JobGetQueryResultsResponse",
    "JobInsertRequest",
    "JobInsertResponse",
    "JobName",
    "JobQueryDoneResponse",
    "JobQueryRequest",
    "JobQueryResponse",
    "JobStatistics",
    "JobStatus",
    "Table",
    "TableDataListRequest",
    "TableDataReadEvent",
    "TableDefinition",
    "TableInfo",
    "TableInsertRequest",
    "TableInsertResponse",
    "TableName",
    "TableUpdateRequest",
    "TableUpdateResponse",
    "TableViewDefinition",
)
