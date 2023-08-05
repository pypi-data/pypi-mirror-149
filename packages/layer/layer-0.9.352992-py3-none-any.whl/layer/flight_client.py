import uuid
from typing import Any, List, Optional, Tuple

from pyarrow import flight

from layer.grpc_utils import create_grpc_ssl_config


class _FlightCallMetadataMiddleware(flight.ClientMiddleware):
    def __init__(self, call_metadata: List[Tuple[str, str]]):
        super().__init__()
        self._call_metadata = call_metadata

    def sending_headers(self) -> Any:
        headers = {i[0]: i[1] for i in self._call_metadata}
        headers["x-request-id"] = str(uuid.uuid4())
        return headers


class _FlightCallMetadataMiddlewareFactory(flight.ClientMiddlewareFactory):
    def __init__(self, call_metadata: List[Tuple[str, str]]):
        super().__init__()
        self._call_metadata = call_metadata

    def start_call(self, info: Any) -> Any:
        return _FlightCallMetadataMiddleware(self._call_metadata)


def _create_flight_client(
    address_and_port: str,
    call_metadata: List[Tuple[str, str]],
    *,
    do_verify_ssl: bool = True,
    hostname_override: Optional[str] = None,
) -> flight.FlightClient:
    location = f"grpc+tls://{address_and_port}"
    middleware = [
        _FlightCallMetadataMiddlewareFactory(call_metadata),
    ]
    ssl_config = create_grpc_ssl_config(
        address_and_port, do_verify_ssl=do_verify_ssl, do_force_cadata_load=True
    )
    hostname = hostname_override if hostname_override else ssl_config.hostname_override
    return flight.FlightClient(
        location=location,
        middleware=middleware,
        tls_root_certs=ssl_config.cadata,
        override_hostname=hostname,
    )
