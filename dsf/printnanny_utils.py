import json
import logging
import os
from base64 import b64encode
from typing import Any, Dict

try:
    from typing import Optional, TypedDict
except ImportError:
    from typing_extensions import TypedDict, Optional

from printnanny_factory_rest_api import ApiClient, AuthApi
from printnanny_factory_rest_api import Configuration as ApiConfiguration
from printnanny_factory_rest_api import OauthTokenRequest

from dsf.connections import CommandConnection

PLUGIN_ID = "PrintNannyDuetPlugin"
DWC_SETTINGS_FILE = "dwc-settings.json"

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


def parse_dwc_settings(settings_file: str):
    pass


def get_system_directory() -> str:
    cmd_conn = CommandConnection()
    cmd_conn.connect()
    res = cmd_conn.resolve_path("0:/sys/")
    cmd_conn.close()
    return res.result


def get_dwc_settings(sys_dir: Optional[str] = None) -> Dict[str, Any]:
    if sys_dir is None:
        sys_dir = get_system_directory()
    dwc_settings_file = os.path.join(sys_dir, DWC_SETTINGS_FILE)
    with open(dwc_settings_file) as f:
        return json.load(f)


def get_credential_file() -> Optional[str]:
    sys_dir = get_system_directory()
    dwc_settings = get_dwc_settings(sys_dir=sys_dir)
    selected = dwc_settings.get("main", {}).get("plugins", {}).get(PLUGIN_ID, {}).get("credentialFile")
    return selected


def load_credentials() -> PluginData:
    credential_file = get_credential_file()
    if not credential_file:
        raise ConfigurationError("No credential file is set")

    with open(credential_file) as f:
        return json.loads(f.read())


async def get_jwt():
    plugin_data = load_credentials()
    client_secret = plugin_data.get("client_secret")
    client_id = plugin_data.get("client_id")
    api_url = plugin_data.get("api_url")
    if client_secret is None:
        raise ConfigurationError("client_secret not set")
    if client_id is None:
        raise ConfigurationError("client_id not set")
    if api_url is None:
        raise ConfigurationError("api_url not set")

    credential = f"{client_id}:{client_secret}"
    encoded_credential = f"Basic {b64encode(credential.encode('utf-8'))}"
    api_config = ApiConfiguration(host=api_url)
    api_client = ApiClient(configuration=api_config)

    api_client.set_default_header("Authorization", encoded_credential)
    auth_api = AuthApi(api_client=api_client)
    request = OauthTokenRequest(grant_type="client_credentials")
    response = await auth_api.o_token_create(request)
    return response
