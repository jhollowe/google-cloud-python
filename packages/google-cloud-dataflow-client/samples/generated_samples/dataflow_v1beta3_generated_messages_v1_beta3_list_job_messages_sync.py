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
# Snippet for ListJobMessages
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dataflow-client


# [START dataflow_v1beta3_generated_MessagesV1Beta3_ListJobMessages_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataflow_v1beta3


def sample_list_job_messages():
    # Create a client
    client = dataflow_v1beta3.MessagesV1Beta3Client()

    # Initialize request argument(s)
    request = dataflow_v1beta3.ListJobMessagesRequest(
    )

    # Make the request
    page_result = client.list_job_messages(request=request)

    # Handle the response
    for response in page_result:
        print(response)

# [END dataflow_v1beta3_generated_MessagesV1Beta3_ListJobMessages_sync]
