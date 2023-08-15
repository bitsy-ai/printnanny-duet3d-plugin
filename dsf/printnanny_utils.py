from base64 import b64encode
from typing import TypedDict

from printnanny_factory_rest_api import ApiClient, AuthApi, OauthTokenRequest

from dsf.commands.object_model import get_object_model

from .error import ConfigurationError

PLUGIN_ID = "PrintNannyDuetPlugin"


class PluginData(TypedDict):
    api_url: str | None
    application_id: str | None
    client_secret: str | None
    client_id: str | None
    printer_id: str | None
    workspace_id: str | None


def get_plugin_data() -> PluginData:
    duet_data = get_object_model()
    plugin_data = duet_data.get("plugins", {}).get(PLUGIN_ID)
    if plugin_data is None:
        raise ConfigurationError(f"plugins.{PLUGIN_ID} not set")
    return PluginData(**plugin_data)


async def get_jwt():
    plugin_data = get_plugin_data()
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
