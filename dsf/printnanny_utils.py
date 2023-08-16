import json
import logging
import os
from base64 import b64encode

try:
    from typing import Optional, TypedDict
except ImportError:
    from typing_extensions import TypedDict, Optional

from printnanny_factory_rest_api import ApiClient, AuthApi, OauthTokenRequest

from dsf.connections import CommandConnection

PLUGIN_ID = "PrintNannyDuetPlugin"

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    pass


class PluginData(TypedDict):
    api_url: Optional[None]
    application_id: Optional[None]
    client_secret: Optional[None]
    client_id: Optional[None]
    printer_id: Optional[None]
    workspace_id: Optional[None]


def load_credentials() -> PluginData:
    cmd_conn = CommandConnection()
    cmd_conn.connect()
    res = cmd_conn.resolve_path(f"0:/sys/{PLUGIN_ID}/")
    cmd_conn.close()
    files = [file for file in os.listdir(res.result) if file.endswith(".json")]
    if len(files) == 0:
        raise ConfigurationError("No credential file found. Upload the .json credentials downloaded from PrintNanny.")
    if len(files) > 1:
        logger.warn(f"Found more than one credential file: {files} Remove stale credentials and try again.")
    credentials_file = files[0]

    with open(credentials_file) as f:
        return json.loads(f.read())


async def get_jwt():
    plugin_data = load_credentials()
    client_secret = plugin_data.get("client_secret")
    client_id = plugin_data.get("client_id")
    if client_secret is None:
        raise ConfigurationError(f"plugins.{PLUGIN_ID}.client_secret not set")
    if client_id is None:
        raise ConfigurationError(f"plugins.{PLUGIN_ID}.client_id not set")

    credential = f"{client_id}:{client_secret}"
    encoded_credential = f"Basic {b64encode(credential.encode('utf-8'))}"
    api_client = ApiClient()

    api_client.set_default_header("Authorization", encoded_credential)
    auth_api = AuthApi(api_client=api_client)
    request = OauthTokenRequest(grant_type="client_credentials")
    response = await auth_api.o_token_create(request)
    return response
