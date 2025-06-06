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
# Generated code. DO NOT EDIT!
#
# Snippet for CreateConversionWorkspace
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dms


# [START datamigration_v1_generated_DataMigrationService_CreateConversionWorkspace_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import clouddms_v1


async def sample_create_conversion_workspace():
    # Create a client
    client = clouddms_v1.DataMigrationServiceAsyncClient()

    # Initialize request argument(s)
    conversion_workspace = clouddms_v1.ConversionWorkspace()
    conversion_workspace.source.engine = "ORACLE"
    conversion_workspace.source.version = "version_value"
    conversion_workspace.destination.engine = "ORACLE"
    conversion_workspace.destination.version = "version_value"

    request = clouddms_v1.CreateConversionWorkspaceRequest(
        parent="parent_value",
        conversion_workspace_id="conversion_workspace_id_value",
        conversion_workspace=conversion_workspace,
    )

    # Make the request
    operation = client.create_conversion_workspace(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END datamigration_v1_generated_DataMigrationService_CreateConversionWorkspace_async]
