from typing import Any

from eth_typing import URI
from requests_auth_aws_sigv4 import AWSSigV4
from web3._utils.request import _get_session
from web3.providers.rpc import HTTPProvider
from web3.types import RPCEndpoint, RPCResponse

aws_auth = AWSSigV4(
    'managedblockchain',
    region="us-east-1"
)


def make_post_request(
        endpoint_uri: URI, data: bytes, *args: Any, **kwargs: Any) -> bytes:
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    # https://github.com/python/mypy/issues/2582
    response = session.post(endpoint_uri, data=data,
                            *args, **kwargs, auth=aws_auth)  # type: ignore
    response.raise_for_status()

    return response.content


class AWSHTTPProvider(HTTPProvider):
    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)

        # .decode() since the AWS sig library expects a string.
        request_data = self.encode_rpc_request(method, params).decode()
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Method: %s, Response: %s",
                          self.endpoint_uri, method, response)
        return response
