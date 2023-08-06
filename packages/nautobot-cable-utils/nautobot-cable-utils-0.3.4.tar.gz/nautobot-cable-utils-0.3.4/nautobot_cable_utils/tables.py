import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ColorColumn, ToggleColumn

from .models import CableTemplate, MeasurementLog

CABLE_LENGTH = """
{% if record.length %}{{ record.length }} {{ record.get_length_unit_display }}{% else %}&mdash;{% endif %}
"""

class CableTemplateTable(BaseTable):
    pk = ToggleColumn()
    cable_number = tables.LinkColumn(
        'plugins:nautobot_cable_utils:cabletemplate_edit', args=[tables.A('pk')],
    )
    type = tables.Column()
    length = tables.TemplateColumn(
        template_code=CABLE_LENGTH,
    )
    color = ColorColumn()
    in_use = tables.TemplateColumn(
        template_code="<span>{% if record.cable %}✔{% else %}✘{% endif %}</span>",
        order_by="cable",
    )

    class Meta(BaseTable.Meta):
        model = CableTemplate
        fields = ('pk', 'cable_number', 'type', 'length', 'color', 'label', 'in_use')
        default_columns = (
            'pk', 'cable_number', 'type', 'length', 'color', 'label', 'in_use'
        )


class MeasurementLogTable(BaseTable):
    pk = ToggleColumn()
    link = tables.LinkColumn(
        'plugins:nautobot_cable_utils:measurement_log_edit', args=[tables.A('pk')],
    )
    cable = tables.LinkColumn('dcim:cable', args=[tables.A('pk')])

    class Meta(BaseTable.Meta):
        model = MeasurementLog
        fields = ('pk', 'link', 'cable')
        default_columns = ('pk', 'link', 'cable')
