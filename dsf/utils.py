from typing import TypedDict

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
        raise ConfigurationError(f"plugins.{PLUGIN_ID} is not defined")
    return PluginData(**plugin_data)
