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
# Snippet for ImportDocuments
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-documentai


# [START documentai_v1beta3_generated_DocumentService_ImportDocuments_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import documentai_v1beta3


def sample_import_documents():
    # Create a client
    client = documentai_v1beta3.DocumentServiceClient()

    # Initialize request argument(s)
    batch_documents_import_configs = documentai_v1beta3.BatchDocumentsImportConfig()
    batch_documents_import_configs.dataset_split = "DATASET_SPLIT_UNASSIGNED"

    request = documentai_v1beta3.ImportDocumentsRequest(
        dataset="dataset_value",
        batch_documents_import_configs=batch_documents_import_configs,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END documentai_v1beta3_generated_DocumentService_ImportDocuments_sync]
