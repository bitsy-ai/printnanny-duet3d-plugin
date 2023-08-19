import json
import logging
from base64 import b64encode
from typing import Any, Dict

try:
    from typing import Optional, TypedDict
except ImportError:
    from typing_extensions import TypedDict, Optional

from printnanny_factory_rest_api import ApiClient, AuthApi
from printnanny_factory_rest_api import Configuration as ApiConfiguration
from printnanny_factory_rest_api import GrantTypeEnum

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


def get_directory(dir: str) -> str:
    cmd_conn = CommandConnection()
    cmd_conn.connect()
    res = cmd_conn.resolve_path(dir)
    cmd_conn.close()
    return res.result


def get_dwc_settings() -> Dict[str, Any]:
    path = get_directory("0:/sys/dwc-settings.json")
    with open(path) as f:
        return json.load(f)


def get_credential_file_path() -> Optional[str]:
    dwc_settings = get_dwc_settings()
    selected = dwc_settings.get("main", {}).get("plugins", {}).get(PLUGIN_ID, {}).get("credentialFile")
    return selected


def load_credentials() -> PluginData:
    credential_file = get_credential_file_path()
    if not credential_file:
        raise ConfigurationError("No credential file is set")

    path = get_directory(credential_file)
    with open(path) as f:
        return json.load(f)


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
    api_key = b64encode(credential.encode("utf-8")).decode("utf-8")
    api_config = ApiConfiguration(host=api_url)
    api_client = ApiClient(configuration=api_config, header_name="Authorization", header_value=f"Basic {api_key}")
    auth_api = AuthApi(api_client=api_client)
    response = await auth_api.o_token_create(GrantTypeEnum.CLIENT_CREDENTIALS)
    return response
