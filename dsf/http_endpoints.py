import socket

from dsf.connections import CommandConnection
from dsf.http import HttpEndpointConnection, HttpEndpointType


async def get_connection_status(http_endpoint_connection: HttpEndpointConnection):
    await http_endpoint_connection.read_request()
    await http_endpoint_connection.send_response(200, "ok")
    http_endpoint_connection.close()


def register_http_endpoints():
    cmd_conn = CommandConnection(debug=True)
    cmd_conn.connect()

    # Register the connection status endpoint
    endpoint = cmd_conn.add_http_endpoint(HttpEndpointType.GET, "printnanny", "connection-status")
    # Register the handler to reply on requests
    endpoint.set_endpoint_handler(get_connection_status)

    hostname = socket.gethostname()
    print(f"Connection status available from http://{hostname}/machine/printnanny/connection-status")

    return cmd_conn, endpoint
