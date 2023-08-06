from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:nautobot_cable_utils:cabletemplate_list',
        link_text='Cable Templates',
        buttons=(
            PluginMenuButton('plugins:nautobot_cable_utils:cabletemplate_add', 'Add Cable Template', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN),
            PluginMenuButton('plugins:nautobot_cable_utils:cabletemplate_import', 'Import Cable Templates', 'mdi mdi-database-import-outline', ButtonColorChoices.BLUE),
        )
    ),
    PluginMenuItem(
        link='plugins:nautobot_cable_utils:measurement_log_list',
        link_text='Measurement Logs',
        buttons=(
            PluginMenuButton('plugins:nautobot_cable_utils:measurement_log_add', 'Add Measurement Log', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN),
        )
    ),
)
