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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflowcx_v3beta1.types import version
from google.cloud.dialogflowcx_v3beta1.types import version as gcdc_version

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseVersionsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class VersionsRestInterceptor:
    """Interceptor for Versions.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the VersionsRestTransport.

    .. code-block:: python
        class MyCustomVersionsInterceptor(VersionsRestInterceptor):
            def pre_compare_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compare_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_load_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_load_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = VersionsRestTransport(interceptor=MyCustomVersionsInterceptor())
        client = VersionsClient(transport=transport)


    """

    def pre_compare_versions(
        self,
        request: version.CompareVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.CompareVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for compare_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_compare_versions(
        self, response: version.CompareVersionsResponse
    ) -> version.CompareVersionsResponse:
        """Post-rpc interceptor for compare_versions

        DEPRECATED. Please use the `post_compare_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_compare_versions` interceptor runs
        before the `post_compare_versions_with_metadata` interceptor.
        """
        return response

    def post_compare_versions_with_metadata(
        self,
        response: version.CompareVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        version.CompareVersionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for compare_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_compare_versions_with_metadata`
        interceptor in new development instead of the `post_compare_versions` interceptor.
        When both interceptors are used, this `post_compare_versions_with_metadata` interceptor runs after the
        `post_compare_versions` interceptor. The (possibly modified) response returned by
        `post_compare_versions` will be passed to
        `post_compare_versions_with_metadata`.
        """
        return response, metadata

    def pre_create_version(
        self,
        request: gcdc_version.CreateVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gcdc_version.CreateVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_create_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_version

        DEPRECATED. Please use the `post_create_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_create_version` interceptor runs
        before the `post_create_version_with_metadata` interceptor.
        """
        return response

    def post_create_version_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_create_version_with_metadata`
        interceptor in new development instead of the `post_create_version` interceptor.
        When both interceptors are used, this `post_create_version_with_metadata` interceptor runs after the
        `post_create_version` interceptor. The (possibly modified) response returned by
        `post_create_version` will be passed to
        `post_create_version_with_metadata`.
        """
        return response, metadata

    def pre_delete_version(
        self,
        request: version.DeleteVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.DeleteVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def pre_get_version(
        self,
        request: version.GetVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.GetVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_get_version(self, response: version.Version) -> version.Version:
        """Post-rpc interceptor for get_version

        DEPRECATED. Please use the `post_get_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_get_version` interceptor runs
        before the `post_get_version_with_metadata` interceptor.
        """
        return response

    def post_get_version_with_metadata(
        self,
        response: version.Version,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.Version, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_get_version_with_metadata`
        interceptor in new development instead of the `post_get_version` interceptor.
        When both interceptors are used, this `post_get_version_with_metadata` interceptor runs after the
        `post_get_version` interceptor. The (possibly modified) response returned by
        `post_get_version` will be passed to
        `post_get_version_with_metadata`.
        """
        return response, metadata

    def pre_list_versions(
        self,
        request: version.ListVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.ListVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_list_versions(
        self, response: version.ListVersionsResponse
    ) -> version.ListVersionsResponse:
        """Post-rpc interceptor for list_versions

        DEPRECATED. Please use the `post_list_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_list_versions` interceptor runs
        before the `post_list_versions_with_metadata` interceptor.
        """
        return response

    def post_list_versions_with_metadata(
        self,
        response: version.ListVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.ListVersionsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_list_versions_with_metadata`
        interceptor in new development instead of the `post_list_versions` interceptor.
        When both interceptors are used, this `post_list_versions_with_metadata` interceptor runs after the
        `post_list_versions` interceptor. The (possibly modified) response returned by
        `post_list_versions` will be passed to
        `post_list_versions_with_metadata`.
        """
        return response, metadata

    def pre_load_version(
        self,
        request: version.LoadVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[version.LoadVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for load_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_load_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for load_version

        DEPRECATED. Please use the `post_load_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_load_version` interceptor runs
        before the `post_load_version_with_metadata` interceptor.
        """
        return response

    def post_load_version_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for load_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_load_version_with_metadata`
        interceptor in new development instead of the `post_load_version` interceptor.
        When both interceptors are used, this `post_load_version_with_metadata` interceptor runs after the
        `post_load_version` interceptor. The (possibly modified) response returned by
        `post_load_version` will be passed to
        `post_load_version_with_metadata`.
        """
        return response, metadata

    def pre_update_version(
        self,
        request: gcdc_version.UpdateVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gcdc_version.UpdateVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_update_version(
        self, response: gcdc_version.Version
    ) -> gcdc_version.Version:
        """Post-rpc interceptor for update_version

        DEPRECATED. Please use the `post_update_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code. This `post_update_version` interceptor runs
        before the `post_update_version_with_metadata` interceptor.
        """
        return response

    def post_update_version_with_metadata(
        self,
        response: gcdc_version.Version,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gcdc_version.Version, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Versions server but before it is returned to user code.

        We recommend only using this `post_update_version_with_metadata`
        interceptor in new development instead of the `post_update_version` interceptor.
        When both interceptors are used, this `post_update_version_with_metadata` interceptor runs after the
        `post_update_version` interceptor. The (possibly modified) response returned by
        `post_update_version` will be passed to
        `post_update_version_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Versions server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Versions server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class VersionsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: VersionsRestInterceptor


class VersionsRestTransport(_BaseVersionsRestTransport):
    """REST backend synchronous transport for Versions.

    Service for managing
    [Versions][google.cloud.dialogflow.cx.v3beta1.Version].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[VersionsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or VersionsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v3beta1/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v3beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CompareVersions(
        _BaseVersionsRestTransport._BaseCompareVersions, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.CompareVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: version.CompareVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> version.CompareVersionsResponse:
            r"""Call the compare versions method over HTTP.

            Args:
                request (~.version.CompareVersionsRequest):
                    The request object. The request message for
                [Versions.CompareVersions][google.cloud.dialogflow.cx.v3beta1.Versions.CompareVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.version.CompareVersionsResponse:
                    The response message for
                [Versions.CompareVersions][google.cloud.dialogflow.cx.v3beta1.Versions.CompareVersions].

            """

            http_options = (
                _BaseVersionsRestTransport._BaseCompareVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_compare_versions(
                request, metadata
            )
            transcoded_request = (
                _BaseVersionsRestTransport._BaseCompareVersions._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseVersionsRestTransport._BaseCompareVersions._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseCompareVersions._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.CompareVersions",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "CompareVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._CompareVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = version.CompareVersionsResponse()
            pb_resp = version.CompareVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_compare_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_compare_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = version.CompareVersionsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.compare_versions",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "CompareVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateVersion(
        _BaseVersionsRestTransport._BaseCreateVersion, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.CreateVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gcdc_version.CreateVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create version method over HTTP.

            Args:
                request (~.gcdc_version.CreateVersionRequest):
                    The request object. The request message for
                [Versions.CreateVersion][google.cloud.dialogflow.cx.v3beta1.Versions.CreateVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseVersionsRestTransport._BaseCreateVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_version(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseCreateVersion._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseVersionsRestTransport._BaseCreateVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseCreateVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.CreateVersion",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "CreateVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._CreateVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_version(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.create_version",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "CreateVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteVersion(
        _BaseVersionsRestTransport._BaseDeleteVersion, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.DeleteVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: version.DeleteVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete version method over HTTP.

            Args:
                request (~.version.DeleteVersionRequest):
                    The request object. The request message for
                [Versions.DeleteVersion][google.cloud.dialogflow.cx.v3beta1.Versions.DeleteVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseDeleteVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_version(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseDeleteVersion._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseDeleteVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.DeleteVersion",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "DeleteVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._DeleteVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetVersion(_BaseVersionsRestTransport._BaseGetVersion, VersionsRestStub):
        def __hash__(self):
            return hash("VersionsRestTransport.GetVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: version.GetVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> version.Version:
            r"""Call the get version method over HTTP.

            Args:
                request (~.version.GetVersionRequest):
                    The request object. The request message for
                [Versions.GetVersion][google.cloud.dialogflow.cx.v3beta1.Versions.GetVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.version.Version:
                    Represents a version of a flow.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseGetVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_version(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseGetVersion._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseGetVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.GetVersion",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._GetVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = version.Version()
            pb_resp = version.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_version(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = version.Version.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.get_version",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListVersions(_BaseVersionsRestTransport._BaseListVersions, VersionsRestStub):
        def __hash__(self):
            return hash("VersionsRestTransport.ListVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: version.ListVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> version.ListVersionsResponse:
            r"""Call the list versions method over HTTP.

            Args:
                request (~.version.ListVersionsRequest):
                    The request object. The request message for
                [Versions.ListVersions][google.cloud.dialogflow.cx.v3beta1.Versions.ListVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.version.ListVersionsResponse:
                    The response message for
                [Versions.ListVersions][google.cloud.dialogflow.cx.v3beta1.Versions.ListVersions].

            """

            http_options = (
                _BaseVersionsRestTransport._BaseListVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_versions(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseListVersions._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseListVersions._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.ListVersions",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._ListVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = version.ListVersionsResponse()
            pb_resp = version.ListVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_versions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = version.ListVersionsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.list_versions",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _LoadVersion(_BaseVersionsRestTransport._BaseLoadVersion, VersionsRestStub):
        def __hash__(self):
            return hash("VersionsRestTransport.LoadVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: version.LoadVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the load version method over HTTP.

            Args:
                request (~.version.LoadVersionRequest):
                    The request object. The request message for
                [Versions.LoadVersion][google.cloud.dialogflow.cx.v3beta1.Versions.LoadVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseVersionsRestTransport._BaseLoadVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_load_version(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseLoadVersion._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseVersionsRestTransport._BaseLoadVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseLoadVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.LoadVersion",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "LoadVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._LoadVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_load_version(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_load_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.load_version",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "LoadVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateVersion(
        _BaseVersionsRestTransport._BaseUpdateVersion, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.UpdateVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gcdc_version.UpdateVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gcdc_version.Version:
            r"""Call the update version method over HTTP.

            Args:
                request (~.gcdc_version.UpdateVersionRequest):
                    The request object. The request message for
                [Versions.UpdateVersion][google.cloud.dialogflow.cx.v3beta1.Versions.UpdateVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gcdc_version.Version:
                    Represents a version of a flow.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseUpdateVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_version(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseUpdateVersion._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseVersionsRestTransport._BaseUpdateVersion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseUpdateVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.UpdateVersion",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "UpdateVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._UpdateVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcdc_version.Version()
            pb_resp = gcdc_version.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_version(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gcdc_version.Version.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsClient.update_version",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "UpdateVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def compare_versions(
        self,
    ) -> Callable[[version.CompareVersionsRequest], version.CompareVersionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompareVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_version(
        self,
    ) -> Callable[[gcdc_version.CreateVersionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_version(
        self,
    ) -> Callable[[version.DeleteVersionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_version(self) -> Callable[[version.GetVersionRequest], version.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_versions(
        self,
    ) -> Callable[[version.ListVersionsRequest], version.ListVersionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def load_version(
        self,
    ) -> Callable[[version.LoadVersionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LoadVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_version(
        self,
    ) -> Callable[[gcdc_version.UpdateVersionRequest], gcdc_version.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseVersionsRestTransport._BaseGetLocation, VersionsRestStub):
        def __hash__(self):
            return hash("VersionsRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseVersionsRestTransport._BaseListLocations, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseVersionsRestTransport._BaseCancelOperation, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseVersionsRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(_BaseVersionsRestTransport._BaseGetOperation, VersionsRestStub):
        def __hash__(self):
            return hash("VersionsRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseVersionsRestTransport._BaseListOperations, VersionsRestStub
    ):
        def __hash__(self):
            return hash("VersionsRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseVersionsRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseVersionsRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVersionsRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.dialogflow.cx_v3beta1.VersionsClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = VersionsRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dialogflow.cx_v3beta1.VersionsAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.dialogflow.cx.v3beta1.Versions",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("VersionsRestTransport",)
