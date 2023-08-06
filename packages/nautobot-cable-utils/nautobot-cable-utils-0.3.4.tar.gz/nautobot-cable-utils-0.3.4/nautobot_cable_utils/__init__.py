from nautobot.extras.plugins import PluginConfig

class CableUtilsConfig(PluginConfig):
    name = 'nautobot_cable_utils'
    verbose_name = 'Cable Utilities'
    description = 'A cable utilities plugin'
    version = "0.3.4"
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot-cable-utils'
    required_settings = [
    ]
    default_settings = {
    }
    middleware = [
    ]

config = CableUtilsConfig
