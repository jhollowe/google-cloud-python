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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.dialogflowcx_v3beta1.services.playbooks import (
    PlaybooksAsyncClient,
    PlaybooksClient,
    pagers,
    transports,
)
from google.cloud.dialogflowcx_v3beta1.types import (
    advanced_settings,
    example,
    fulfillment,
    gcs,
    generative_settings,
    parameter_definition,
)
from google.cloud.dialogflowcx_v3beta1.types import playbook
from google.cloud.dialogflowcx_v3beta1.types import playbook as gcdc_playbook
from google.cloud.dialogflowcx_v3beta1.types import response_message, tool_call

CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert PlaybooksClient._get_default_mtls_endpoint(None) is None
    assert PlaybooksClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        PlaybooksClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PlaybooksClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PlaybooksClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert PlaybooksClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert PlaybooksClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert PlaybooksClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert PlaybooksClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            PlaybooksClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert PlaybooksClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert PlaybooksClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert PlaybooksClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            PlaybooksClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert PlaybooksClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert PlaybooksClient._get_client_cert_source(None, False) is None
    assert (
        PlaybooksClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        PlaybooksClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                PlaybooksClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                PlaybooksClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    PlaybooksClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksClient),
)
@mock.patch.object(
    PlaybooksAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = PlaybooksClient._DEFAULT_UNIVERSE
    default_endpoint = PlaybooksClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = PlaybooksClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        PlaybooksClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        PlaybooksClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == PlaybooksClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PlaybooksClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        PlaybooksClient._get_api_endpoint(None, None, default_universe, "always")
        == PlaybooksClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PlaybooksClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == PlaybooksClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PlaybooksClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        PlaybooksClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        PlaybooksClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        PlaybooksClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        PlaybooksClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        PlaybooksClient._get_universe_domain(None, None)
        == PlaybooksClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        PlaybooksClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = PlaybooksClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = PlaybooksClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (PlaybooksClient, "grpc"),
        (PlaybooksAsyncClient, "grpc_asyncio"),
        (PlaybooksClient, "rest"),
    ],
)
def test_playbooks_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "dialogflow.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dialogflow.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.PlaybooksGrpcTransport, "grpc"),
        (transports.PlaybooksGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.PlaybooksRestTransport, "rest"),
    ],
)
def test_playbooks_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (PlaybooksClient, "grpc"),
        (PlaybooksAsyncClient, "grpc_asyncio"),
        (PlaybooksClient, "rest"),
    ],
)
def test_playbooks_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "dialogflow.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dialogflow.googleapis.com"
        )


def test_playbooks_client_get_transport_class():
    transport = PlaybooksClient.get_transport_class()
    available_transports = [
        transports.PlaybooksGrpcTransport,
        transports.PlaybooksRestTransport,
    ]
    assert transport in available_transports

    transport = PlaybooksClient.get_transport_class("grpc")
    assert transport == transports.PlaybooksGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc"),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (PlaybooksClient, transports.PlaybooksRestTransport, "rest"),
    ],
)
@mock.patch.object(
    PlaybooksClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksClient),
)
@mock.patch.object(
    PlaybooksAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksAsyncClient),
)
def test_playbooks_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(PlaybooksClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(PlaybooksClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc", "true"),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc", "false"),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (PlaybooksClient, transports.PlaybooksRestTransport, "rest", "true"),
        (PlaybooksClient, transports.PlaybooksRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    PlaybooksClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksClient),
)
@mock.patch.object(
    PlaybooksAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_playbooks_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [PlaybooksClient, PlaybooksAsyncClient])
@mock.patch.object(
    PlaybooksClient, "DEFAULT_ENDPOINT", modify_default_endpoint(PlaybooksClient)
)
@mock.patch.object(
    PlaybooksAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PlaybooksAsyncClient),
)
def test_playbooks_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [PlaybooksClient, PlaybooksAsyncClient])
@mock.patch.object(
    PlaybooksClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksClient),
)
@mock.patch.object(
    PlaybooksAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PlaybooksAsyncClient),
)
def test_playbooks_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = PlaybooksClient._DEFAULT_UNIVERSE
    default_endpoint = PlaybooksClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = PlaybooksClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc"),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (PlaybooksClient, transports.PlaybooksRestTransport, "rest"),
    ],
)
def test_playbooks_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc", grpc_helpers),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (PlaybooksClient, transports.PlaybooksRestTransport, "rest", None),
    ],
)
def test_playbooks_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_playbooks_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.playbooks.transports.PlaybooksGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = PlaybooksClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport, "grpc", grpc_helpers),
        (
            PlaybooksAsyncClient,
            transports.PlaybooksGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_playbooks_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "dialogflow.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=None,
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_playbook.CreatePlaybookRequest,
        dict,
    ],
)
def test_create_playbook(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )
        response = client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcdc_playbook.CreatePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


def test_create_playbook_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcdc_playbook.CreatePlaybookRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_playbook(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_playbook.CreatePlaybookRequest(
            parent="parent_value",
        )


def test_create_playbook_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_playbook] = mock_rpc
        request = {}
        client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_playbook_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_playbook
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_playbook
        ] = mock_rpc

        request = {}
        await client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_playbook_async(
    transport: str = "grpc_asyncio", request_type=gcdc_playbook.CreatePlaybookRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        response = await client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcdc_playbook.CreatePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.asyncio
async def test_create_playbook_async_from_dict():
    await test_create_playbook_async(request_type=dict)


def test_create_playbook_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_playbook.CreatePlaybookRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        call.return_value = gcdc_playbook.Playbook()
        client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_playbook_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_playbook.CreatePlaybookRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook()
        )
        await client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_playbook_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_playbook(
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].playbook
        mock_val = gcdc_playbook.Playbook(name="name_value")
        assert arg == mock_val


def test_create_playbook_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_playbook(
            gcdc_playbook.CreatePlaybookRequest(),
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_playbook_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_playbook(
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].playbook
        mock_val = gcdc_playbook.Playbook(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_playbook_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_playbook(
            gcdc_playbook.CreatePlaybookRequest(),
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.DeletePlaybookRequest,
        dict,
    ],
)
def test_delete_playbook(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.DeletePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_playbook_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.DeletePlaybookRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_playbook(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.DeletePlaybookRequest(
            name="name_value",
        )


def test_delete_playbook_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_playbook] = mock_rpc
        request = {}
        client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_playbook_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_playbook
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_playbook
        ] = mock_rpc

        request = {}
        await client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_playbook_async(
    transport: str = "grpc_asyncio", request_type=playbook.DeletePlaybookRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.DeletePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_playbook_async_from_dict():
    await test_delete_playbook_async(request_type=dict)


def test_delete_playbook_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.DeletePlaybookRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        call.return_value = None
        client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_playbook_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.DeletePlaybookRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_playbook_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_playbook(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_playbook_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_playbook(
            playbook.DeletePlaybookRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_playbook_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_playbook(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_playbook_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_playbook(
            playbook.DeletePlaybookRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.ListPlaybooksRequest,
        dict,
    ],
)
def test_list_playbooks(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybooksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.ListPlaybooksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybooksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_playbooks_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.ListPlaybooksRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_playbooks(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.ListPlaybooksRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_playbooks_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_playbooks in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_playbooks] = mock_rpc
        request = {}
        client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_playbooks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_playbooks_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_playbooks
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_playbooks
        ] = mock_rpc

        request = {}
        await client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_playbooks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_playbooks_async(
    transport: str = "grpc_asyncio", request_type=playbook.ListPlaybooksRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybooksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.ListPlaybooksRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybooksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_playbooks_async_from_dict():
    await test_list_playbooks_async(request_type=dict)


def test_list_playbooks_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.ListPlaybooksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        call.return_value = playbook.ListPlaybooksResponse()
        client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_playbooks_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.ListPlaybooksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybooksResponse()
        )
        await client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_playbooks_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybooksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_playbooks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_playbooks_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_playbooks(
            playbook.ListPlaybooksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_playbooks_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybooksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybooksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_playbooks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_playbooks_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_playbooks(
            playbook.ListPlaybooksRequest(),
            parent="parent_value",
        )


def test_list_playbooks_pager(transport_name: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[],
                next_page_token="def",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_playbooks(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, playbook.Playbook) for i in results)


def test_list_playbooks_pages(transport_name: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[],
                next_page_token="def",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_playbooks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_playbooks_async_pager():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbooks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[],
                next_page_token="def",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_playbooks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, playbook.Playbook) for i in responses)


@pytest.mark.asyncio
async def test_list_playbooks_async_pages():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbooks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[],
                next_page_token="def",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_playbooks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.GetPlaybookRequest,
        dict,
    ],
)
def test_get_playbook(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )
        response = client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.GetPlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


def test_get_playbook_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.GetPlaybookRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_playbook(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.GetPlaybookRequest(
            name="name_value",
        )


def test_get_playbook_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_playbook] = mock_rpc
        request = {}
        client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_playbook_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_playbook
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_playbook
        ] = mock_rpc

        request = {}
        await client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_playbook_async(
    transport: str = "grpc_asyncio", request_type=playbook.GetPlaybookRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        response = await client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.GetPlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.asyncio
async def test_get_playbook_async_from_dict():
    await test_get_playbook_async(request_type=dict)


def test_get_playbook_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.GetPlaybookRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        call.return_value = playbook.Playbook()
        client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_playbook_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.GetPlaybookRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(playbook.Playbook())
        await client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_playbook_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.Playbook()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_playbook(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_playbook_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_playbook(
            playbook.GetPlaybookRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_playbook_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.Playbook()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(playbook.Playbook())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_playbook(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_playbook_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_playbook(
            playbook.GetPlaybookRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_playbook.UpdatePlaybookRequest,
        dict,
    ],
)
def test_update_playbook(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )
        response = client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcdc_playbook.UpdatePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


def test_update_playbook_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcdc_playbook.UpdatePlaybookRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_playbook(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_playbook.UpdatePlaybookRequest()


def test_update_playbook_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_playbook] = mock_rpc
        request = {}
        client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_playbook_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_playbook
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_playbook
        ] = mock_rpc

        request = {}
        await client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_playbook_async(
    transport: str = "grpc_asyncio", request_type=gcdc_playbook.UpdatePlaybookRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        response = await client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcdc_playbook.UpdatePlaybookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.asyncio
async def test_update_playbook_async_from_dict():
    await test_update_playbook_async(request_type=dict)


def test_update_playbook_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_playbook.UpdatePlaybookRequest()

    request.playbook.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        call.return_value = gcdc_playbook.Playbook()
        client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "playbook.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_playbook_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_playbook.UpdatePlaybookRequest()

    request.playbook.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook()
        )
        await client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "playbook.name=name_value",
    ) in kw["metadata"]


def test_update_playbook_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_playbook(
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].playbook
        mock_val = gcdc_playbook.Playbook(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_playbook_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_playbook(
            gcdc_playbook.UpdatePlaybookRequest(),
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_playbook_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_playbook.Playbook()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_playbook(
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].playbook
        mock_val = gcdc_playbook.Playbook(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_playbook_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_playbook(
            gcdc_playbook.UpdatePlaybookRequest(),
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.CreatePlaybookVersionRequest,
        dict,
    ],
)
def test_create_playbook_version(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion(
            name="name_value",
            description="description_value",
        )
        response = client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.CreatePlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_create_playbook_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.CreatePlaybookVersionRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_playbook_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.CreatePlaybookVersionRequest(
            parent="parent_value",
        )


def test_create_playbook_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_playbook_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_playbook_version
        ] = mock_rpc
        request = {}
        client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_playbook_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_playbook_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_playbook_version
        ] = mock_rpc

        request = {}
        await client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_playbook_version_async(
    transport: str = "grpc_asyncio", request_type=playbook.CreatePlaybookVersionRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.CreatePlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_playbook_version_async_from_dict():
    await test_create_playbook_version_async(request_type=dict)


def test_create_playbook_version_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.CreatePlaybookVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        call.return_value = playbook.PlaybookVersion()
        client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_playbook_version_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.CreatePlaybookVersionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion()
        )
        await client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_playbook_version_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_playbook_version(
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].playbook_version
        mock_val = playbook.PlaybookVersion(name="name_value")
        assert arg == mock_val


def test_create_playbook_version_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_playbook_version(
            playbook.CreatePlaybookVersionRequest(),
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_playbook_version_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_playbook_version(
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].playbook_version
        mock_val = playbook.PlaybookVersion(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_playbook_version_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_playbook_version(
            playbook.CreatePlaybookVersionRequest(),
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.GetPlaybookVersionRequest,
        dict,
    ],
)
def test_get_playbook_version(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion(
            name="name_value",
            description="description_value",
        )
        response = client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.GetPlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_playbook_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.GetPlaybookVersionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_playbook_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.GetPlaybookVersionRequest(
            name="name_value",
        )


def test_get_playbook_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_playbook_version in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_playbook_version
        ] = mock_rpc
        request = {}
        client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_playbook_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_playbook_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_playbook_version
        ] = mock_rpc

        request = {}
        await client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_playbook_version_async(
    transport: str = "grpc_asyncio", request_type=playbook.GetPlaybookVersionRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.GetPlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_playbook_version_async_from_dict():
    await test_get_playbook_version_async(request_type=dict)


def test_get_playbook_version_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.GetPlaybookVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        call.return_value = playbook.PlaybookVersion()
        client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_playbook_version_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.GetPlaybookVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion()
        )
        await client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_playbook_version_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_playbook_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_playbook_version_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_playbook_version(
            playbook.GetPlaybookVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_playbook_version_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.PlaybookVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_playbook_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_playbook_version_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_playbook_version(
            playbook.GetPlaybookVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.ListPlaybookVersionsRequest,
        dict,
    ],
)
def test_list_playbook_versions(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybookVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.ListPlaybookVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybookVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_playbook_versions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.ListPlaybookVersionsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_playbook_versions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.ListPlaybookVersionsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_playbook_versions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_playbook_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_playbook_versions
        ] = mock_rpc
        request = {}
        client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_playbook_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_playbook_versions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_playbook_versions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_playbook_versions
        ] = mock_rpc

        request = {}
        await client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_playbook_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_playbook_versions_async(
    transport: str = "grpc_asyncio", request_type=playbook.ListPlaybookVersionsRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybookVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.ListPlaybookVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybookVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_playbook_versions_async_from_dict():
    await test_list_playbook_versions_async(request_type=dict)


def test_list_playbook_versions_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.ListPlaybookVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        call.return_value = playbook.ListPlaybookVersionsResponse()
        client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_playbook_versions_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.ListPlaybookVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybookVersionsResponse()
        )
        await client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_playbook_versions_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybookVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_playbook_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_playbook_versions_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_playbook_versions(
            playbook.ListPlaybookVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_playbook_versions_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = playbook.ListPlaybookVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybookVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_playbook_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_playbook_versions_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_playbook_versions(
            playbook.ListPlaybookVersionsRequest(),
            parent="parent_value",
        )


def test_list_playbook_versions_pager(transport_name: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[],
                next_page_token="def",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_playbook_versions(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, playbook.PlaybookVersion) for i in results)


def test_list_playbook_versions_pages(transport_name: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[],
                next_page_token="def",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_playbook_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_playbook_versions_async_pager():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[],
                next_page_token="def",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_playbook_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, playbook.PlaybookVersion) for i in responses)


@pytest.mark.asyncio
async def test_list_playbook_versions_async_pages():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[],
                next_page_token="def",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_playbook_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.DeletePlaybookVersionRequest,
        dict,
    ],
)
def test_delete_playbook_version(request_type, transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = playbook.DeletePlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_playbook_version_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = playbook.DeletePlaybookVersionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_playbook_version(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == playbook.DeletePlaybookVersionRequest(
            name="name_value",
        )


def test_delete_playbook_version_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_playbook_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_playbook_version
        ] = mock_rpc
        request = {}
        client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_playbook_version_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = PlaybooksAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_playbook_version
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_playbook_version
        ] = mock_rpc

        request = {}
        await client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_playbook_version_async(
    transport: str = "grpc_asyncio", request_type=playbook.DeletePlaybookVersionRequest
):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = playbook.DeletePlaybookVersionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_playbook_version_async_from_dict():
    await test_delete_playbook_version_async(request_type=dict)


def test_delete_playbook_version_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.DeletePlaybookVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        call.return_value = None
        client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_playbook_version_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = playbook.DeletePlaybookVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_playbook_version_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_playbook_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_playbook_version_flattened_error():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_playbook_version(
            playbook.DeletePlaybookVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_playbook_version_flattened_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_playbook_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_playbook_version_flattened_error_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_playbook_version(
            playbook.DeletePlaybookVersionRequest(),
            name="name_value",
        )


def test_create_playbook_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_playbook] = mock_rpc

        request = {}
        client.create_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_playbook_rest_required_fields(
    request_type=gcdc_playbook.CreatePlaybookRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcdc_playbook.Playbook()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcdc_playbook.Playbook.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_playbook(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_playbook_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_playbook._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "playbook",
            )
        )
    )


def test_create_playbook_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcdc_playbook.Playbook()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcdc_playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_playbook(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*}/playbooks"
            % client.transport._host,
            args[1],
        )


def test_create_playbook_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_playbook(
            gcdc_playbook.CreatePlaybookRequest(),
            parent="parent_value",
            playbook=gcdc_playbook.Playbook(name="name_value"),
        )


def test_delete_playbook_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_playbook] = mock_rpc

        request = {}
        client.delete_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_playbook_rest_required_fields(
    request_type=playbook.DeletePlaybookRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_playbook(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_playbook_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_playbook._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_delete_playbook_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_playbook(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_playbook_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_playbook(
            playbook.DeletePlaybookRequest(),
            name="name_value",
        )


def test_list_playbooks_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_playbooks in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_playbooks] = mock_rpc

        request = {}
        client.list_playbooks(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_playbooks(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_playbooks_rest_required_fields(
    request_type=playbook.ListPlaybooksRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_playbooks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_playbooks._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = playbook.ListPlaybooksResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = playbook.ListPlaybooksResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_playbooks(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_playbooks_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_playbooks._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_playbooks_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.ListPlaybooksResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = playbook.ListPlaybooksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_playbooks(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*}/playbooks"
            % client.transport._host,
            args[1],
        )


def test_list_playbooks_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_playbooks(
            playbook.ListPlaybooksRequest(),
            parent="parent_value",
        )


def test_list_playbooks_rest_pager(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[],
                next_page_token="def",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybooksResponse(
                playbooks=[
                    playbook.Playbook(),
                    playbook.Playbook(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(playbook.ListPlaybooksResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        pager = client.list_playbooks(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, playbook.Playbook) for i in results)

        pages = list(client.list_playbooks(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_playbook_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_playbook] = mock_rpc

        request = {}
        client.get_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_playbook_rest_required_fields(request_type=playbook.GetPlaybookRequest):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = playbook.Playbook()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = playbook.Playbook.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_playbook(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_playbook_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_playbook._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_playbook_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.Playbook()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_playbook(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*}"
            % client.transport._host,
            args[1],
        )


def test_get_playbook_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_playbook(
            playbook.GetPlaybookRequest(),
            name="name_value",
        )


def test_update_playbook_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_playbook in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_playbook] = mock_rpc

        request = {}
        client.update_playbook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_playbook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_playbook_rest_required_fields(
    request_type=gcdc_playbook.UpdatePlaybookRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_playbook._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_playbook._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcdc_playbook.Playbook()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcdc_playbook.Playbook.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_playbook(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_playbook_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_playbook._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("playbook",)))


def test_update_playbook_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcdc_playbook.Playbook()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "playbook": {
                "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcdc_playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_playbook(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{playbook.name=projects/*/locations/*/agents/*/playbooks/*}"
            % client.transport._host,
            args[1],
        )


def test_update_playbook_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_playbook(
            gcdc_playbook.UpdatePlaybookRequest(),
            playbook=gcdc_playbook.Playbook(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_playbook_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_playbook_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_playbook_version
        ] = mock_rpc

        request = {}
        client.create_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_playbook_version_rest_required_fields(
    request_type=playbook.CreatePlaybookVersionRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = playbook.PlaybookVersion()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = playbook.PlaybookVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_playbook_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_playbook_version_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_playbook_version._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "playbookVersion",
            )
        )
    )


def test_create_playbook_version_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.PlaybookVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = playbook.PlaybookVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_playbook_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*/playbooks/*}/versions"
            % client.transport._host,
            args[1],
        )


def test_create_playbook_version_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_playbook_version(
            playbook.CreatePlaybookVersionRequest(),
            parent="parent_value",
            playbook_version=playbook.PlaybookVersion(name="name_value"),
        )


def test_get_playbook_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_playbook_version in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_playbook_version
        ] = mock_rpc

        request = {}
        client.get_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_playbook_version_rest_required_fields(
    request_type=playbook.GetPlaybookVersionRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = playbook.PlaybookVersion()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = playbook.PlaybookVersion.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_playbook_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_playbook_version_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_playbook_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_playbook_version_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.PlaybookVersion()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = playbook.PlaybookVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_playbook_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_playbook_version_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_playbook_version(
            playbook.GetPlaybookVersionRequest(),
            name="name_value",
        )


def test_list_playbook_versions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_playbook_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_playbook_versions
        ] = mock_rpc

        request = {}
        client.list_playbook_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_playbook_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_playbook_versions_rest_required_fields(
    request_type=playbook.ListPlaybookVersionsRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_playbook_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_playbook_versions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = playbook.ListPlaybookVersionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = playbook.ListPlaybookVersionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_playbook_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_playbook_versions_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_playbook_versions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_playbook_versions_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.ListPlaybookVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = playbook.ListPlaybookVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_playbook_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*/playbooks/*}/versions"
            % client.transport._host,
            args[1],
        )


def test_list_playbook_versions_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_playbook_versions(
            playbook.ListPlaybookVersionsRequest(),
            parent="parent_value",
        )


def test_list_playbook_versions_rest_pager(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
                next_page_token="abc",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[],
                next_page_token="def",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                ],
                next_page_token="ghi",
            ),
            playbook.ListPlaybookVersionsResponse(
                playbook_versions=[
                    playbook.PlaybookVersion(),
                    playbook.PlaybookVersion(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            playbook.ListPlaybookVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }

        pager = client.list_playbook_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, playbook.PlaybookVersion) for i in results)

        pages = list(client.list_playbook_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_playbook_version_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_playbook_version
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_playbook_version
        ] = mock_rpc

        request = {}
        client.delete_playbook_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_playbook_version(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_playbook_version_rest_required_fields(
    request_type=playbook.DeletePlaybookVersionRequest,
):
    transport_class = transports.PlaybooksRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_playbook_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_playbook_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_playbook_version_rest_unset_required_fields():
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_playbook_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_delete_playbook_version_rest_flattened():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_playbook_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/playbooks/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_playbook_version_rest_flattened_error(transport: str = "rest"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_playbook_version(
            playbook.DeletePlaybookVersionRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PlaybooksClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PlaybooksClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PlaybooksClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PlaybooksClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = PlaybooksClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PlaybooksGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.PlaybooksGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PlaybooksGrpcTransport,
        transports.PlaybooksGrpcAsyncIOTransport,
        transports.PlaybooksRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = PlaybooksClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_playbook_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        call.return_value = gcdc_playbook.Playbook()
        client.create_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.CreatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_playbook_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        call.return_value = None
        client.delete_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_playbooks_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        call.return_value = playbook.ListPlaybooksResponse()
        client.list_playbooks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybooksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_playbook_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        call.return_value = playbook.Playbook()
        client.get_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_playbook_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        call.return_value = gcdc_playbook.Playbook()
        client.update_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.UpdatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_playbook_version_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        call.return_value = playbook.PlaybookVersion()
        client.create_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.CreatePlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_playbook_version_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        call.return_value = playbook.PlaybookVersion()
        client.get_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_playbook_versions_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        call.return_value = playbook.ListPlaybookVersionsResponse()
        client.list_playbook_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybookVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_playbook_version_empty_call_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        call.return_value = None
        client.delete_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookVersionRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = PlaybooksAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_playbook_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        await client.create_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.CreatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_playbook_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_playbooks_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybooksResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_playbooks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybooksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_playbook_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        await client.get_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_playbook_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_playbook.Playbook(
                name="name_value",
                display_name="display_name_value",
                goal="goal_value",
                token_count=1193,
                referenced_playbooks=["referenced_playbooks_value"],
                referenced_flows=["referenced_flows_value"],
                referenced_tools=["referenced_tools_value"],
            )
        )
        await client.update_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.UpdatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_playbook_version_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion(
                name="name_value",
                description="description_value",
            )
        )
        await client.create_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.CreatePlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_playbook_version_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.PlaybookVersion(
                name="name_value",
                description="description_value",
            )
        )
        await client.get_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_playbook_versions_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            playbook.ListPlaybookVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_playbook_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybookVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_playbook_version_empty_call_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookVersionRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = PlaybooksClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_create_playbook_rest_bad_request(
    request_type=gcdc_playbook.CreatePlaybookRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_playbook(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_playbook.CreatePlaybookRequest,
        dict,
    ],
)
def test_create_playbook_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request_init["playbook"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "goal": "goal_value",
        "input_parameter_definitions": [
            {"name": "name_value", "type_": 1, "description": "description_value"}
        ],
        "output_parameter_definitions": {},
        "instruction": {
            "guidelines": "guidelines_value",
            "steps": [{"text": "text_value", "steps": {}}],
        },
        "token_count": 1193,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "referenced_playbooks": [
            "referenced_playbooks_value1",
            "referenced_playbooks_value2",
        ],
        "referenced_flows": ["referenced_flows_value1", "referenced_flows_value2"],
        "referenced_tools": ["referenced_tools_value1", "referenced_tools_value2"],
        "llm_model_settings": {
            "model": "model_value",
            "prompt_text": "prompt_text_value",
        },
        "speech_settings": {
            "endpointer_sensitivity": 2402,
            "no_speech_timeout": {"seconds": 751, "nanos": 543},
            "use_timeout_based_endpointing": True,
            "models": {},
        },
        "handlers": [
            {
                "event_handler": {
                    "event": "event_value",
                    "condition": "condition_value",
                    "fulfillment": {
                        "messages": [
                            {
                                "text": {
                                    "text": ["text_value1", "text_value2"],
                                    "allow_playback_interruption": True,
                                },
                                "payload": {"fields": {}},
                                "conversation_success": {"metadata": {}},
                                "output_audio_text": {
                                    "text": "text_value",
                                    "ssml": "ssml_value",
                                    "allow_playback_interruption": True,
                                },
                                "live_agent_handoff": {"metadata": {}},
                                "end_interaction": {},
                                "play_audio": {
                                    "audio_uri": "audio_uri_value",
                                    "allow_playback_interruption": True,
                                },
                                "mixed_audio": {
                                    "segments": [
                                        {
                                            "audio": b"audio_blob",
                                            "uri": "uri_value",
                                            "allow_playback_interruption": True,
                                        }
                                    ]
                                },
                                "telephony_transfer_call": {
                                    "phone_number": "phone_number_value"
                                },
                                "knowledge_info_card": {},
                                "tool_call": {
                                    "tool": "tool_value",
                                    "action": "action_value",
                                    "input_parameters": {},
                                },
                                "channel": "channel_value",
                            }
                        ],
                        "webhook": "webhook_value",
                        "return_partial_responses": True,
                        "tag": "tag_value",
                        "set_parameter_actions": [
                            {
                                "parameter": "parameter_value",
                                "value": {
                                    "null_value": 0,
                                    "number_value": 0.1285,
                                    "string_value": "string_value_value",
                                    "bool_value": True,
                                    "struct_value": {},
                                    "list_value": {"values": {}},
                                },
                            }
                        ],
                        "conditional_cases": [
                            {
                                "cases": [
                                    {
                                        "condition": "condition_value",
                                        "case_content": [
                                            {"message": {}, "additional_cases": {}}
                                        ],
                                    }
                                ]
                            }
                        ],
                        "advanced_settings": {
                            "audio_export_gcs_destination": {"uri": "uri_value"},
                            "speech_settings": {},
                            "dtmf_settings": {
                                "enabled": True,
                                "max_digits": 1065,
                                "finish_digit": "finish_digit_value",
                                "interdigit_timeout_duration": {},
                                "endpointing_timeout_duration": {},
                            },
                            "logging_settings": {
                                "enable_stackdriver_logging": True,
                                "enable_interaction_logging": True,
                                "enable_consent_based_redaction": True,
                            },
                        },
                        "enable_generative_fallback": True,
                    },
                },
                "lifecycle_handler": {
                    "lifecycle_stage": "lifecycle_stage_value",
                    "condition": "condition_value",
                    "fulfillment": {},
                },
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcdc_playbook.CreatePlaybookRequest.meta.fields["playbook"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["playbook"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["playbook"][field])):
                    del request_init["playbook"][field][i][subfield]
            else:
                del request_init["playbook"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcdc_playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcdc_playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_playbook(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_playbook_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_create_playbook"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_create_playbook_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_create_playbook"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcdc_playbook.CreatePlaybookRequest.pb(
            gcdc_playbook.CreatePlaybookRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcdc_playbook.Playbook.to_json(gcdc_playbook.Playbook())
        req.return_value.content = return_value

        request = gcdc_playbook.CreatePlaybookRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcdc_playbook.Playbook()
        post_with_metadata.return_value = gcdc_playbook.Playbook(), metadata

        client.create_playbook(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_playbook_rest_bad_request(request_type=playbook.DeletePlaybookRequest):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_playbook(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.DeletePlaybookRequest,
        dict,
    ],
)
def test_delete_playbook_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.delete_playbook(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_playbook_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_delete_playbook"
    ) as pre:
        pre.assert_not_called()
        pb_message = playbook.DeletePlaybookRequest.pb(playbook.DeletePlaybookRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        request = playbook.DeletePlaybookRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_playbook(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_list_playbooks_rest_bad_request(request_type=playbook.ListPlaybooksRequest):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_playbooks(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.ListPlaybooksRequest,
        dict,
    ],
)
def test_list_playbooks_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.ListPlaybooksResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = playbook.ListPlaybooksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_playbooks(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybooksPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_playbooks_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_list_playbooks"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_list_playbooks_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_list_playbooks"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = playbook.ListPlaybooksRequest.pb(playbook.ListPlaybooksRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = playbook.ListPlaybooksResponse.to_json(
            playbook.ListPlaybooksResponse()
        )
        req.return_value.content = return_value

        request = playbook.ListPlaybooksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = playbook.ListPlaybooksResponse()
        post_with_metadata.return_value = playbook.ListPlaybooksResponse(), metadata

        client.list_playbooks(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_playbook_rest_bad_request(request_type=playbook.GetPlaybookRequest):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_playbook(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.GetPlaybookRequest,
        dict,
    ],
)
def test_get_playbook_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_playbook(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_playbook_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_get_playbook"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_get_playbook_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_get_playbook"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = playbook.GetPlaybookRequest.pb(playbook.GetPlaybookRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = playbook.Playbook.to_json(playbook.Playbook())
        req.return_value.content = return_value

        request = playbook.GetPlaybookRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = playbook.Playbook()
        post_with_metadata.return_value = playbook.Playbook(), metadata

        client.get_playbook(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_update_playbook_rest_bad_request(
    request_type=gcdc_playbook.UpdatePlaybookRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "playbook": {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.update_playbook(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_playbook.UpdatePlaybookRequest,
        dict,
    ],
)
def test_update_playbook_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "playbook": {
            "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
        }
    }
    request_init["playbook"] = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4",
        "display_name": "display_name_value",
        "goal": "goal_value",
        "input_parameter_definitions": [
            {"name": "name_value", "type_": 1, "description": "description_value"}
        ],
        "output_parameter_definitions": {},
        "instruction": {
            "guidelines": "guidelines_value",
            "steps": [{"text": "text_value", "steps": {}}],
        },
        "token_count": 1193,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "referenced_playbooks": [
            "referenced_playbooks_value1",
            "referenced_playbooks_value2",
        ],
        "referenced_flows": ["referenced_flows_value1", "referenced_flows_value2"],
        "referenced_tools": ["referenced_tools_value1", "referenced_tools_value2"],
        "llm_model_settings": {
            "model": "model_value",
            "prompt_text": "prompt_text_value",
        },
        "speech_settings": {
            "endpointer_sensitivity": 2402,
            "no_speech_timeout": {"seconds": 751, "nanos": 543},
            "use_timeout_based_endpointing": True,
            "models": {},
        },
        "handlers": [
            {
                "event_handler": {
                    "event": "event_value",
                    "condition": "condition_value",
                    "fulfillment": {
                        "messages": [
                            {
                                "text": {
                                    "text": ["text_value1", "text_value2"],
                                    "allow_playback_interruption": True,
                                },
                                "payload": {"fields": {}},
                                "conversation_success": {"metadata": {}},
                                "output_audio_text": {
                                    "text": "text_value",
                                    "ssml": "ssml_value",
                                    "allow_playback_interruption": True,
                                },
                                "live_agent_handoff": {"metadata": {}},
                                "end_interaction": {},
                                "play_audio": {
                                    "audio_uri": "audio_uri_value",
                                    "allow_playback_interruption": True,
                                },
                                "mixed_audio": {
                                    "segments": [
                                        {
                                            "audio": b"audio_blob",
                                            "uri": "uri_value",
                                            "allow_playback_interruption": True,
                                        }
                                    ]
                                },
                                "telephony_transfer_call": {
                                    "phone_number": "phone_number_value"
                                },
                                "knowledge_info_card": {},
                                "tool_call": {
                                    "tool": "tool_value",
                                    "action": "action_value",
                                    "input_parameters": {},
                                },
                                "channel": "channel_value",
                            }
                        ],
                        "webhook": "webhook_value",
                        "return_partial_responses": True,
                        "tag": "tag_value",
                        "set_parameter_actions": [
                            {
                                "parameter": "parameter_value",
                                "value": {
                                    "null_value": 0,
                                    "number_value": 0.1285,
                                    "string_value": "string_value_value",
                                    "bool_value": True,
                                    "struct_value": {},
                                    "list_value": {"values": {}},
                                },
                            }
                        ],
                        "conditional_cases": [
                            {
                                "cases": [
                                    {
                                        "condition": "condition_value",
                                        "case_content": [
                                            {"message": {}, "additional_cases": {}}
                                        ],
                                    }
                                ]
                            }
                        ],
                        "advanced_settings": {
                            "audio_export_gcs_destination": {"uri": "uri_value"},
                            "speech_settings": {},
                            "dtmf_settings": {
                                "enabled": True,
                                "max_digits": 1065,
                                "finish_digit": "finish_digit_value",
                                "interdigit_timeout_duration": {},
                                "endpointing_timeout_duration": {},
                            },
                            "logging_settings": {
                                "enable_stackdriver_logging": True,
                                "enable_interaction_logging": True,
                                "enable_consent_based_redaction": True,
                            },
                        },
                        "enable_generative_fallback": True,
                    },
                },
                "lifecycle_handler": {
                    "lifecycle_stage": "lifecycle_stage_value",
                    "condition": "condition_value",
                    "fulfillment": {},
                },
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcdc_playbook.UpdatePlaybookRequest.meta.fields["playbook"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["playbook"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["playbook"][field])):
                    del request_init["playbook"][field][i][subfield]
            else:
                del request_init["playbook"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcdc_playbook.Playbook(
            name="name_value",
            display_name="display_name_value",
            goal="goal_value",
            token_count=1193,
            referenced_playbooks=["referenced_playbooks_value"],
            referenced_flows=["referenced_flows_value"],
            referenced_tools=["referenced_tools_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcdc_playbook.Playbook.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_playbook(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_playbook.Playbook)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.goal == "goal_value"
    assert response.token_count == 1193
    assert response.referenced_playbooks == ["referenced_playbooks_value"]
    assert response.referenced_flows == ["referenced_flows_value"]
    assert response.referenced_tools == ["referenced_tools_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_playbook_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_update_playbook"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_update_playbook_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_update_playbook"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcdc_playbook.UpdatePlaybookRequest.pb(
            gcdc_playbook.UpdatePlaybookRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcdc_playbook.Playbook.to_json(gcdc_playbook.Playbook())
        req.return_value.content = return_value

        request = gcdc_playbook.UpdatePlaybookRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcdc_playbook.Playbook()
        post_with_metadata.return_value = gcdc_playbook.Playbook(), metadata

        client.update_playbook(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_playbook_version_rest_bad_request(
    request_type=playbook.CreatePlaybookVersionRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_playbook_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.CreatePlaybookVersionRequest,
        dict,
    ],
)
def test_create_playbook_version_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request_init["playbook_version"] = {
        "name": "name_value",
        "description": "description_value",
        "playbook": {
            "name": "name_value",
            "display_name": "display_name_value",
            "goal": "goal_value",
            "input_parameter_definitions": [
                {"name": "name_value", "type_": 1, "description": "description_value"}
            ],
            "output_parameter_definitions": {},
            "instruction": {
                "guidelines": "guidelines_value",
                "steps": [{"text": "text_value", "steps": {}}],
            },
            "token_count": 1193,
            "create_time": {"seconds": 751, "nanos": 543},
            "update_time": {},
            "referenced_playbooks": [
                "referenced_playbooks_value1",
                "referenced_playbooks_value2",
            ],
            "referenced_flows": ["referenced_flows_value1", "referenced_flows_value2"],
            "referenced_tools": ["referenced_tools_value1", "referenced_tools_value2"],
            "llm_model_settings": {
                "model": "model_value",
                "prompt_text": "prompt_text_value",
            },
            "speech_settings": {
                "endpointer_sensitivity": 2402,
                "no_speech_timeout": {"seconds": 751, "nanos": 543},
                "use_timeout_based_endpointing": True,
                "models": {},
            },
            "handlers": [
                {
                    "event_handler": {
                        "event": "event_value",
                        "condition": "condition_value",
                        "fulfillment": {
                            "messages": [
                                {
                                    "text": {
                                        "text": ["text_value1", "text_value2"],
                                        "allow_playback_interruption": True,
                                    },
                                    "payload": {"fields": {}},
                                    "conversation_success": {"metadata": {}},
                                    "output_audio_text": {
                                        "text": "text_value",
                                        "ssml": "ssml_value",
                                        "allow_playback_interruption": True,
                                    },
                                    "live_agent_handoff": {"metadata": {}},
                                    "end_interaction": {},
                                    "play_audio": {
                                        "audio_uri": "audio_uri_value",
                                        "allow_playback_interruption": True,
                                    },
                                    "mixed_audio": {
                                        "segments": [
                                            {
                                                "audio": b"audio_blob",
                                                "uri": "uri_value",
                                                "allow_playback_interruption": True,
                                            }
                                        ]
                                    },
                                    "telephony_transfer_call": {
                                        "phone_number": "phone_number_value"
                                    },
                                    "knowledge_info_card": {},
                                    "tool_call": {
                                        "tool": "tool_value",
                                        "action": "action_value",
                                        "input_parameters": {},
                                    },
                                    "channel": "channel_value",
                                }
                            ],
                            "webhook": "webhook_value",
                            "return_partial_responses": True,
                            "tag": "tag_value",
                            "set_parameter_actions": [
                                {
                                    "parameter": "parameter_value",
                                    "value": {
                                        "null_value": 0,
                                        "number_value": 0.1285,
                                        "string_value": "string_value_value",
                                        "bool_value": True,
                                        "struct_value": {},
                                        "list_value": {"values": {}},
                                    },
                                }
                            ],
                            "conditional_cases": [
                                {
                                    "cases": [
                                        {
                                            "condition": "condition_value",
                                            "case_content": [
                                                {"message": {}, "additional_cases": {}}
                                            ],
                                        }
                                    ]
                                }
                            ],
                            "advanced_settings": {
                                "audio_export_gcs_destination": {"uri": "uri_value"},
                                "speech_settings": {},
                                "dtmf_settings": {
                                    "enabled": True,
                                    "max_digits": 1065,
                                    "finish_digit": "finish_digit_value",
                                    "interdigit_timeout_duration": {},
                                    "endpointing_timeout_duration": {},
                                },
                                "logging_settings": {
                                    "enable_stackdriver_logging": True,
                                    "enable_interaction_logging": True,
                                    "enable_consent_based_redaction": True,
                                },
                            },
                            "enable_generative_fallback": True,
                        },
                    },
                    "lifecycle_handler": {
                        "lifecycle_stage": "lifecycle_stage_value",
                        "condition": "condition_value",
                        "fulfillment": {},
                    },
                }
            ],
        },
        "examples": [
            {
                "name": "name_value",
                "playbook_input": {
                    "preceding_conversation_summary": "preceding_conversation_summary_value",
                    "action_parameters": {},
                },
                "playbook_output": {
                    "execution_summary": "execution_summary_value",
                    "action_parameters": {},
                },
                "actions": [
                    {
                        "user_utterance": {"text": "text_value"},
                        "agent_utterance": {"text": "text_value"},
                        "tool_use": {
                            "tool": "tool_value",
                            "display_name": "display_name_value",
                            "action": "action_value",
                            "input_action_parameters": {},
                            "output_action_parameters": {},
                        },
                        "playbook_invocation": {
                            "playbook": "playbook_value",
                            "display_name": "display_name_value",
                            "playbook_input": {},
                            "playbook_output": {},
                            "playbook_state": 1,
                        },
                        "flow_invocation": {
                            "flow": "flow_value",
                            "display_name": "display_name_value",
                            "input_action_parameters": {},
                            "output_action_parameters": {},
                            "flow_state": 1,
                        },
                    }
                ],
                "display_name": "display_name_value",
                "description": "description_value",
                "token_count": 1193,
                "create_time": {},
                "update_time": {},
                "conversation_state": 1,
                "language_code": "language_code_value",
            }
        ],
        "update_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = playbook.CreatePlaybookVersionRequest.meta.fields["playbook_version"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["playbook_version"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["playbook_version"][field])):
                    del request_init["playbook_version"][field][i][subfield]
            else:
                del request_init["playbook_version"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.PlaybookVersion(
            name="name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = playbook.PlaybookVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_playbook_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_playbook_version_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_create_playbook_version"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor,
        "post_create_playbook_version_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_create_playbook_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = playbook.CreatePlaybookVersionRequest.pb(
            playbook.CreatePlaybookVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = playbook.PlaybookVersion.to_json(playbook.PlaybookVersion())
        req.return_value.content = return_value

        request = playbook.CreatePlaybookVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = playbook.PlaybookVersion()
        post_with_metadata.return_value = playbook.PlaybookVersion(), metadata

        client.create_playbook_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_playbook_version_rest_bad_request(
    request_type=playbook.GetPlaybookVersionRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_playbook_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.GetPlaybookVersionRequest,
        dict,
    ],
)
def test_get_playbook_version_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.PlaybookVersion(
            name="name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = playbook.PlaybookVersion.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_playbook_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, playbook.PlaybookVersion)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_playbook_version_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_get_playbook_version"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_get_playbook_version_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_get_playbook_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = playbook.GetPlaybookVersionRequest.pb(
            playbook.GetPlaybookVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = playbook.PlaybookVersion.to_json(playbook.PlaybookVersion())
        req.return_value.content = return_value

        request = playbook.GetPlaybookVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = playbook.PlaybookVersion()
        post_with_metadata.return_value = playbook.PlaybookVersion(), metadata

        client.get_playbook_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_playbook_versions_rest_bad_request(
    request_type=playbook.ListPlaybookVersionsRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_playbook_versions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.ListPlaybookVersionsRequest,
        dict,
    ],
)
def test_list_playbook_versions_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = playbook.ListPlaybookVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = playbook.ListPlaybookVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_playbook_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPlaybookVersionsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_playbook_versions_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_list_playbook_versions"
    ) as post, mock.patch.object(
        transports.PlaybooksRestInterceptor, "post_list_playbook_versions_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_list_playbook_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = playbook.ListPlaybookVersionsRequest.pb(
            playbook.ListPlaybookVersionsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = playbook.ListPlaybookVersionsResponse.to_json(
            playbook.ListPlaybookVersionsResponse()
        )
        req.return_value.content = return_value

        request = playbook.ListPlaybookVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = playbook.ListPlaybookVersionsResponse()
        post_with_metadata.return_value = (
            playbook.ListPlaybookVersionsResponse(),
            metadata,
        )

        client.list_playbook_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_playbook_version_rest_bad_request(
    request_type=playbook.DeletePlaybookVersionRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_playbook_version(request)


@pytest.mark.parametrize(
    "request_type",
    [
        playbook.DeletePlaybookVersionRequest,
        dict,
    ],
)
def test_delete_playbook_version_rest_call_success(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/playbooks/sample4/versions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.delete_playbook_version(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_playbook_version_rest_interceptors(null_interceptor):
    transport = transports.PlaybooksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.PlaybooksRestInterceptor(),
    )
    client = PlaybooksClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PlaybooksRestInterceptor, "pre_delete_playbook_version"
    ) as pre:
        pre.assert_not_called()
        pb_message = playbook.DeletePlaybookVersionRequest.pb(
            playbook.DeletePlaybookVersionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        request = playbook.DeletePlaybookVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_playbook_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_get_location_rest_bad_request(request_type=locations_pb2.GetLocationRequest):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    request_type=locations_pb2.ListLocationsRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_cancel_operation_rest_bad_request(
    request_type=operations_pb2.CancelOperationRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/operations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/operations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = "{}"
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/operations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/operations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    request_type=operations_pb2.ListOperationsRequest,
):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_initialize_client_w_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_playbook_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_playbook), "__call__") as call:
        client.create_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.CreatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_playbook_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_playbook), "__call__") as call:
        client.delete_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_playbooks_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_playbooks), "__call__") as call:
        client.list_playbooks(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybooksRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_playbook_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_playbook), "__call__") as call:
        client.get_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_playbook_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.update_playbook), "__call__") as call:
        client.update_playbook(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_playbook.UpdatePlaybookRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_playbook_version_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_playbook_version), "__call__"
    ) as call:
        client.create_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.CreatePlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_playbook_version_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_playbook_version), "__call__"
    ) as call:
        client.get_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.GetPlaybookVersionRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_playbook_versions_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_playbook_versions), "__call__"
    ) as call:
        client.list_playbook_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.ListPlaybookVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_playbook_version_empty_call_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_playbook_version), "__call__"
    ) as call:
        client.delete_playbook_version(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = playbook.DeletePlaybookVersionRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.PlaybooksGrpcTransport,
    )


def test_playbooks_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.PlaybooksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_playbooks_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.playbooks.transports.PlaybooksTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PlaybooksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_playbook",
        "delete_playbook",
        "list_playbooks",
        "get_playbook",
        "update_playbook",
        "create_playbook_version",
        "get_playbook_version",
        "list_playbook_versions",
        "delete_playbook_version",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_playbooks_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.playbooks.transports.PlaybooksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PlaybooksTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_playbooks_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.playbooks.transports.PlaybooksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PlaybooksTransport()
        adc.assert_called_once()


def test_playbooks_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        PlaybooksClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PlaybooksGrpcTransport,
        transports.PlaybooksGrpcAsyncIOTransport,
    ],
)
def test_playbooks_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PlaybooksGrpcTransport,
        transports.PlaybooksGrpcAsyncIOTransport,
        transports.PlaybooksRestTransport,
    ],
)
def test_playbooks_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.PlaybooksGrpcTransport, grpc_helpers),
        (transports.PlaybooksGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_playbooks_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "dialogflow.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=["1", "2"],
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.PlaybooksGrpcTransport, transports.PlaybooksGrpcAsyncIOTransport],
)
def test_playbooks_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_playbooks_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.PlaybooksRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_playbooks_host_no_port(transport_name):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dialogflow.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dialogflow.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_playbooks_host_with_port(transport_name):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dialogflow.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dialogflow.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_playbooks_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = PlaybooksClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = PlaybooksClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_playbook._session
    session2 = client2.transport.create_playbook._session
    assert session1 != session2
    session1 = client1.transport.delete_playbook._session
    session2 = client2.transport.delete_playbook._session
    assert session1 != session2
    session1 = client1.transport.list_playbooks._session
    session2 = client2.transport.list_playbooks._session
    assert session1 != session2
    session1 = client1.transport.get_playbook._session
    session2 = client2.transport.get_playbook._session
    assert session1 != session2
    session1 = client1.transport.update_playbook._session
    session2 = client2.transport.update_playbook._session
    assert session1 != session2
    session1 = client1.transport.create_playbook_version._session
    session2 = client2.transport.create_playbook_version._session
    assert session1 != session2
    session1 = client1.transport.get_playbook_version._session
    session2 = client2.transport.get_playbook_version._session
    assert session1 != session2
    session1 = client1.transport.list_playbook_versions._session
    session2 = client2.transport.list_playbook_versions._session
    assert session1 != session2
    session1 = client1.transport.delete_playbook_version._session
    session2 = client2.transport.delete_playbook_version._session
    assert session1 != session2


def test_playbooks_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PlaybooksGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_playbooks_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PlaybooksGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.PlaybooksGrpcTransport, transports.PlaybooksGrpcAsyncIOTransport],
)
def test_playbooks_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.PlaybooksGrpcTransport, transports.PlaybooksGrpcAsyncIOTransport],
)
def test_playbooks_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_example_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    playbook = "octopus"
    example = "oyster"
    expected = "projects/{project}/locations/{location}/agents/{agent}/playbooks/{playbook}/examples/{example}".format(
        project=project,
        location=location,
        agent=agent,
        playbook=playbook,
        example=example,
    )
    actual = PlaybooksClient.example_path(project, location, agent, playbook, example)
    assert expected == actual


def test_parse_example_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "agent": "mussel",
        "playbook": "winkle",
        "example": "nautilus",
    }
    path = PlaybooksClient.example_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_example_path(path)
    assert expected == actual


def test_flow_path():
    project = "scallop"
    location = "abalone"
    agent = "squid"
    flow = "clam"
    expected = (
        "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}".format(
            project=project,
            location=location,
            agent=agent,
            flow=flow,
        )
    )
    actual = PlaybooksClient.flow_path(project, location, agent, flow)
    assert expected == actual


def test_parse_flow_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "agent": "oyster",
        "flow": "nudibranch",
    }
    path = PlaybooksClient.flow_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_flow_path(path)
    assert expected == actual


def test_playbook_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    playbook = "nautilus"
    expected = "projects/{project}/locations/{location}/agents/{agent}/playbooks/{playbook}".format(
        project=project,
        location=location,
        agent=agent,
        playbook=playbook,
    )
    actual = PlaybooksClient.playbook_path(project, location, agent, playbook)
    assert expected == actual


def test_parse_playbook_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "agent": "squid",
        "playbook": "clam",
    }
    path = PlaybooksClient.playbook_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_playbook_path(path)
    assert expected == actual


def test_playbook_version_path():
    project = "whelk"
    location = "octopus"
    agent = "oyster"
    playbook = "nudibranch"
    version = "cuttlefish"
    expected = "projects/{project}/locations/{location}/agents/{agent}/playbooks/{playbook}/versions/{version}".format(
        project=project,
        location=location,
        agent=agent,
        playbook=playbook,
        version=version,
    )
    actual = PlaybooksClient.playbook_version_path(
        project, location, agent, playbook, version
    )
    assert expected == actual


def test_parse_playbook_version_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "agent": "nautilus",
        "playbook": "scallop",
        "version": "abalone",
    }
    path = PlaybooksClient.playbook_version_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_playbook_version_path(path)
    assert expected == actual


def test_tool_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    tool = "octopus"
    expected = (
        "projects/{project}/locations/{location}/agents/{agent}/tools/{tool}".format(
            project=project,
            location=location,
            agent=agent,
            tool=tool,
        )
    )
    actual = PlaybooksClient.tool_path(project, location, agent, tool)
    assert expected == actual


def test_parse_tool_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "agent": "cuttlefish",
        "tool": "mussel",
    }
    path = PlaybooksClient.tool_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_tool_path(path)
    assert expected == actual


def test_webhook_path():
    project = "winkle"
    location = "nautilus"
    agent = "scallop"
    webhook = "abalone"
    expected = "projects/{project}/locations/{location}/agents/{agent}/webhooks/{webhook}".format(
        project=project,
        location=location,
        agent=agent,
        webhook=webhook,
    )
    actual = PlaybooksClient.webhook_path(project, location, agent, webhook)
    assert expected == actual


def test_parse_webhook_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "agent": "whelk",
        "webhook": "octopus",
    }
    path = PlaybooksClient.webhook_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_webhook_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = PlaybooksClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = PlaybooksClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = PlaybooksClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = PlaybooksClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = PlaybooksClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = PlaybooksClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = PlaybooksClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = PlaybooksClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = PlaybooksClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = PlaybooksClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = PlaybooksClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.PlaybooksTransport, "_prep_wrapped_messages"
    ) as prep:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.PlaybooksTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = PlaybooksClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_cancel_operation(transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc_asyncio"):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = PlaybooksClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = PlaybooksAsyncClient(credentials=async_anonymous_credentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close_grpc():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = PlaybooksAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = PlaybooksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = PlaybooksClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (PlaybooksClient, transports.PlaybooksGrpcTransport),
        (PlaybooksAsyncClient, transports.PlaybooksGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
