#!/usr/bin/env python3

"""
Subscribe to changed in Duet3D object model and re-publish PrintNanny Factory events

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""
import json

from dsf.connections import SubscribeConnection, SubscriptionMode

# from .http_endpoints import register_http_endpoints


def subscribe_to_duet_model():
    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
    subscribe_connection.connect()

    try:
        # Get the complete model once
        object_model = subscribe_connection.get_object_model()

        print(f"{object_model}")

        # Get multiple incremental updates, due to SubscriptionMode.PATCH, only a
        # subset of the object model will be updated
        for _ in range(0, 300):
            update = json.loads(subscribe_connection.get_object_model_patch())
            print(f"{update}")
    finally:
        subscribe_connection.close()


if __name__ == "__main__":
    subscribe_to_duet_model()
    # try:
    #     cmd_conn, endpoint = register_http_endpoints()
    #     subscribe_to_duet_model()
    # finally:
    #     if endpoint is not None:
    #         endpoint.close()
    #     cmd_conn.close()
