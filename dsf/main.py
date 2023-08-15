#!/usr/bin/env python3

"""
Subscribe to changed in Duet3D object model
and re-publish PrintNanny Factory events

Make sure when running this script to have access to the
DSF UNIX socket owned by the dsf user.
"""
import socket

from printnanny_utils import get_jwt

from dsf.connections import CommandConnection, SubscribeConnection, SubscriptionMode
from dsf.http import HttpEndpointConnection, HttpEndpointType


async def get_connection_status(endpoint: HttpEndpointConnection):
    jwt = get_jwt()
    await endpoint.send_response(200, jwt)
    endpoint.close()


def register_http_endpoints():
    cmd_conn = CommandConnection(debug=True)
    cmd_conn.connect()

    # Register the connection status endpoint
    endpoint = cmd_conn.add_http_endpoint(HttpEndpointType.GET, "printnanny", "connection-status")
    # Register the handler to reply on requests
    endpoint.set_endpoint_handler(get_connection_status)

    hostname = socket.gethostname()
    url = f"http://{hostname}/machine/printnanny/connection-status"
    print(f"Connection status available from {url}")

    return cmd_conn, endpoint


def subscribe_to_duet_model():
    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
    subscribe_connection.connect()

    try:
        # Get the complete model once
        object_model = subscribe_connection.get_object_model()

        print(f"{object_model}")
    finally:
        subscribe_connection.close()


if __name__ == "__main__":
    subscribe_to_duet_model()
    try:
        cmd_conn, endpoint = register_http_endpoints()
        subscribe_to_duet_model()
    finally:
        if endpoint is not None:
            endpoint.close()
        cmd_conn.close()
