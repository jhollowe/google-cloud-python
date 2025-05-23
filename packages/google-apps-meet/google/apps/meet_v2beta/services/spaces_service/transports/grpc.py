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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.apps.meet_v2beta.types import resource, service

from .base import DEFAULT_CLIENT_INFO, SpacesServiceTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.apps.meet.v2beta.SpacesService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.apps.meet.v2beta.SpacesService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class SpacesServiceGrpcTransport(SpacesServiceTransport):
    """gRPC backend transport for SpacesService.

    REST API for services dealing with spaces.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'meet.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def create_space(self) -> Callable[[service.CreateSpaceRequest], resource.Space]:
        r"""Return a callable for the create space method over gRPC.

        Creates a space.

        Returns:
            Callable[[~.CreateSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_space" not in self._stubs:
            self._stubs["create_space"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/CreateSpace",
                request_serializer=service.CreateSpaceRequest.serialize,
                response_deserializer=resource.Space.deserialize,
            )
        return self._stubs["create_space"]

    @property
    def get_space(self) -> Callable[[service.GetSpaceRequest], resource.Space]:
        r"""Return a callable for the get space method over gRPC.

        Gets details about a meeting space.

        For an example, see `Get a meeting
        space <https://developers.google.com/meet/api/guides/meeting-spaces#get-meeting-space>`__.

        Returns:
            Callable[[~.GetSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space" not in self._stubs:
            self._stubs["get_space"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/GetSpace",
                request_serializer=service.GetSpaceRequest.serialize,
                response_deserializer=resource.Space.deserialize,
            )
        return self._stubs["get_space"]

    @property
    def update_space(self) -> Callable[[service.UpdateSpaceRequest], resource.Space]:
        r"""Return a callable for the update space method over gRPC.

        Updates details about a meeting space.

        For an example, see `Update a meeting
        space <https://developers.google.com/meet/api/guides/meeting-spaces#update-meeting-space>`__.

        Returns:
            Callable[[~.UpdateSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_space" not in self._stubs:
            self._stubs["update_space"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/UpdateSpace",
                request_serializer=service.UpdateSpaceRequest.serialize,
                response_deserializer=resource.Space.deserialize,
            )
        return self._stubs["update_space"]

    @property
    def connect_active_conference(
        self,
    ) -> Callable[
        [service.ConnectActiveConferenceRequest],
        service.ConnectActiveConferenceResponse,
    ]:
        r"""Return a callable for the connect active conference method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__:
        Broker a WebRTC connection to the active conference of a space.

        On success, clients must use the resulting SDP (Session
        Description Protocol) answer to establish a WebRTC connection.
        Once connected, additional functionality is available across
        WebRTC data channels.

        See `Meet Media API
        overview <https://developers.google.com/meet/media-api/guides/overview>`__
        for more details about this connection.

        Returns:
            Callable[[~.ConnectActiveConferenceRequest],
                    ~.ConnectActiveConferenceResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "connect_active_conference" not in self._stubs:
            self._stubs["connect_active_conference"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/ConnectActiveConference",
                request_serializer=service.ConnectActiveConferenceRequest.serialize,
                response_deserializer=service.ConnectActiveConferenceResponse.deserialize,
            )
        return self._stubs["connect_active_conference"]

    @property
    def end_active_conference(
        self,
    ) -> Callable[[service.EndActiveConferenceRequest], empty_pb2.Empty]:
        r"""Return a callable for the end active conference method over gRPC.

        Ends an active conference (if there's one).

        For an example, see `End active
        conference <https://developers.google.com/meet/api/guides/meeting-spaces#end-active-conference>`__.

        Returns:
            Callable[[~.EndActiveConferenceRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "end_active_conference" not in self._stubs:
            self._stubs["end_active_conference"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/EndActiveConference",
                request_serializer=service.EndActiveConferenceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["end_active_conference"]

    @property
    def create_member(self) -> Callable[[service.CreateMemberRequest], resource.Member]:
        r"""Return a callable for the create member method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__:
        Create a member.

        This API supports the ``fields`` parameter in
        `SystemParameterContext <https://cloud.google.com/apis/docs/system-parameters>`__.
        When the ``fields`` parameter is omitted, this API response will
        default to "name,email,role,user".

        Returns:
            Callable[[~.CreateMemberRequest],
                    ~.Member]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_member" not in self._stubs:
            self._stubs["create_member"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/CreateMember",
                request_serializer=service.CreateMemberRequest.serialize,
                response_deserializer=resource.Member.deserialize,
            )
        return self._stubs["create_member"]

    @property
    def get_member(self) -> Callable[[service.GetMemberRequest], resource.Member]:
        r"""Return a callable for the get member method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__:
        Get a member.

        This API supports the ``fields`` parameter in
        `SystemParameterContext <https://cloud.google.com/apis/docs/system-parameters>`__.
        When the ``fields`` parameter is omitted, this API response will
        default to "name,email,role,user".

        Returns:
            Callable[[~.GetMemberRequest],
                    ~.Member]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_member" not in self._stubs:
            self._stubs["get_member"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/GetMember",
                request_serializer=service.GetMemberRequest.serialize,
                response_deserializer=resource.Member.deserialize,
            )
        return self._stubs["get_member"]

    @property
    def list_members(
        self,
    ) -> Callable[[service.ListMembersRequest], service.ListMembersResponse]:
        r"""Return a callable for the list members method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__:
        List members.

        This API supports the ``fields`` parameter in
        `SystemParameterContext <https://cloud.google.com/apis/docs/system-parameters>`__.
        When the ``fields`` parameter is omitted this API response will
        default to "name,email,role,user".

        Returns:
            Callable[[~.ListMembersRequest],
                    ~.ListMembersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_members" not in self._stubs:
            self._stubs["list_members"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/ListMembers",
                request_serializer=service.ListMembersRequest.serialize,
                response_deserializer=service.ListMembersResponse.deserialize,
            )
        return self._stubs["list_members"]

    @property
    def delete_member(self) -> Callable[[service.DeleteMemberRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete member method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__:
        Delete the member who was previously assigned roles in the
        space.

        Returns:
            Callable[[~.DeleteMemberRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_member" not in self._stubs:
            self._stubs["delete_member"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.SpacesService/DeleteMember",
                request_serializer=service.DeleteMemberRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_member"]

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("SpacesServiceGrpcTransport",)
