#!/usr/bin/env python3

"""
Subscribe to changed in Duet3D object model
and re-publish PrintNanny Factory events

Make sure when running this script to have access to the
DSF UNIX socket owned by the dsf user.
"""
import json
import traceback

from printnanny_utils import ConfigurationError, get_jwt, get_printer

from dsf.connections import CommandConnection, SubscribeConnection, SubscriptionMode
from dsf.http import HttpEndpointConnection, HttpEndpointType


async def get_connection_status(endpoint: HttpEndpointConnection):
    try:
        jwt = await get_jwt()
        response = dict(access_token=False, printer_endpoint=False)
        access_token = jwt.get("access_token")
        if access_token is not None:
            response["access_token"] = True
            printer = await get_printer(jwt=jwt["access_token"])
            if printer.id:
                response["printer"] = True

        await endpoint.send_response(200, response)
    except ConfigurationError as e:
        await endpoint.send_response(400, json.dumps({"error": str(e)}))
    except Exception as e:
        tb = "".join(traceback.format_exc())
        await endpoint.send_response(500, json.dumps({"error": str(e), "traceback": tb}))


def register_http_endpoints(cmd_conn):
    # Register the connection status endpoint
    endpoint = cmd_conn.add_http_endpoint(HttpEndpointType.GET, "printnanny", "connection-status")
    # Register the handler to reply on requests
    endpoint.set_endpoint_handler(get_connection_status)

    return endpoint


def subscribe_to_duet_model():
    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
    subscribe_connection.connect()

    try:
        # Get the complete model once
        object_model = subscribe_connection.get_object_model()

        print(f"{object_model}")
        while True:
            pass
    finally:
        subscribe_connection.close()


if __name__ == "__main__":
    cmd_conn = CommandConnection()
    try:
        cmd_conn.connect()
        endpoint = register_http_endpoints(cmd_conn)
        subscribe_to_duet_model()
    finally:
        if endpoint is not None:
            endpoint.close()
        cmd_conn.close()
