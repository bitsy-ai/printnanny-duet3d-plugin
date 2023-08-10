import socket

from dsf.connections import CommandConnection
from dsf.http import HttpEndpointConnection, HttpEndpointType


async def get_connection_status(endpoint: HttpEndpointConnection):
    await endpoint.read_request()
    await endpoint.send_response(200, "ok")
    endpoint.close()


def register_http_endpoints():
    cmd_conn = CommandConnection(debug=True)
    cmd_conn.connect()

    # Register the connection status endpoint
    endpoint = cmd_conn.add_http_endpoint(
        HttpEndpointType.GET, "printnanny", "connection-status"
    )
    # Register the handler to reply on requests
    endpoint.set_endpoint_handler(get_connection_status)

    hostname = socket.gethostname()
    url = f"http://{hostname}/machine/printnanny/connection-status"
    print(f"Connection status available from {url}")

    return cmd_conn, endpoint
