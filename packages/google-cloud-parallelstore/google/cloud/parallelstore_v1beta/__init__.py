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
from google.cloud.parallelstore_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.parallelstore import ParallelstoreAsyncClient, ParallelstoreClient
from .types.parallelstore import (
    CreateInstanceRequest,
    DeleteInstanceRequest,
    DeploymentType,
    DestinationGcsBucket,
    DestinationParallelstore,
    DirectoryStripeLevel,
    ExportDataMetadata,
    ExportDataRequest,
    ExportDataResponse,
    FileStripeLevel,
    GetInstanceRequest,
    ImportDataMetadata,
    ImportDataRequest,
    ImportDataResponse,
    Instance,
    ListInstancesRequest,
    ListInstancesResponse,
    OperationMetadata,
    SourceGcsBucket,
    SourceParallelstore,
    TransferCounters,
    TransferErrorLogEntry,
    TransferErrorSummary,
    TransferMetadataOptions,
    TransferOperationMetadata,
    TransferType,
    UpdateInstanceRequest,
)

__all__ = (
    "ParallelstoreAsyncClient",
    "CreateInstanceRequest",
    "DeleteInstanceRequest",
    "DeploymentType",
    "DestinationGcsBucket",
    "DestinationParallelstore",
    "DirectoryStripeLevel",
    "ExportDataMetadata",
    "ExportDataRequest",
    "ExportDataResponse",
    "FileStripeLevel",
    "GetInstanceRequest",
    "ImportDataMetadata",
    "ImportDataRequest",
    "ImportDataResponse",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "OperationMetadata",
    "ParallelstoreClient",
    "SourceGcsBucket",
    "SourceParallelstore",
    "TransferCounters",
    "TransferErrorLogEntry",
    "TransferErrorSummary",
    "TransferMetadataOptions",
    "TransferOperationMetadata",
    "TransferType",
    "UpdateInstanceRequest",
)
