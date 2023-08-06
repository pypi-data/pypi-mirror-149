from logging import PlaceHolder
from multiprocessing.managers import ValueProxy
from django import forms

from nautobot.circuits.models import Circuit, CircuitTermination, Provider
from nautobot.dcim.choices import CableStatusChoices, CableTypeChoices
from nautobot.dcim.models import (
    Cable, ConsolePort, ConsoleServerPort, Device, FrontPort, Interface,
    PowerFeed, PowerOutlet, PowerPanel, PowerPort, Rack, RearPort,
    Site,
)

from nautobot.extras.models import Status

from nautobot.utilities.forms import (
    APISelect, BootstrapMixin, ColorSelect, CSVModelForm,
    DynamicModelChoiceField, StaticSelect2, add_blank_choice
)

from .models import CableTemplate, MeasurementLog
from django.core.exceptions import ObjectDoesNotExist


class ConnectCableToDeviceForm(BootstrapMixin, forms.ModelForm):
    """
    Base form for connecting a Cable to a Device component
    """
    termination_a_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False,
    )
    termination_a_rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        label='Rack',
        required=False,
        display_field='display_name',
        null_option='None',
        query_params={
            'site_id': '$termination_a_site'
        }
    )
    termination_a_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label='Device',
        required=False,
        display_field='display_name',
        query_params={
            'site_id': '$termination_a_site',
            'rack_id': '$termination_a_rack',
        }
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_b_rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        label='Rack',
        required=False,
        display_field='display_name',
        null_option='None',
        query_params={
            'site_id': '$termination_b_site'
        }
    )
    termination_b_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label='Device',
        required=False,
        display_field='display_name',
        query_params={
            'site_id': '$termination_b_site',
            'rack_id': '$termination_b_rack',
        }
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_site', 'termination_a_rack', 'termination_a_device', 'termination_a_id',
            'termination_b_site', 'termination_b_rack', 'termination_b_device', 'termination_b_id'
        ]

    def clean_termination_a_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_a_id'], 'pk', None)

    def clean_termination_b_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_b_id'], 'pk', None)


class ConnectConsolePortToConsoleServerPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=ConsolePort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=ConsoleServerPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectConsolePortToFrontPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=ConsolePort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectConsolePortToRearPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=ConsolePort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectConsoleServerPortToFrontPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=ConsoleServerPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectConsoleServerPortToRearPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=ConsoleServerPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectPowerfeedToPowerPortForm(ConnectCableToDeviceForm):
    termination_a_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False,
        display_field='cid'
    )
    termination_a_powerpanel = DynamicModelChoiceField(
        queryset=PowerPanel.objects.all(),
        label='Power Panel',
        required=False,
        query_params={
            'site_id': '$termination_a_site',
        }
    )
    termination_a_id = DynamicModelChoiceField(
        queryset=PowerFeed.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'power_panel_id': '$termination_a_powerpanel'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=PowerPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_site', 'termination_a_powerpanel', 'termination_a_id',
            'termination_b_site', 'termination_b_rack', 'termination_b_device', 'termination_b_id'
        ]


class ConnectPowerOutletToPowerPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=PowerOutlet.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=PowerPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectInterfaceForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device',
            'kind': 'physical',
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device',
            'kind': 'physical',
        }
    )


class ConnectFrontPortToInterfaceForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device',
            'kind': 'physical',
        }
    )


class ConnectInterfaceToRearPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device',
            'kind': 'physical',
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCircuitTerminationToInterfaceForm(ConnectCableToDeviceForm):
    termination_a_provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='Provider',
        required=False
    )
    termination_a_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_a_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        label='Circuit',
        display_field='cid',
        query_params={
            'provider_id': '$termination_a_provider',
            'site_id': '$termination_a_site',
        }
    )
    termination_a_id = DynamicModelChoiceField(
        queryset=CircuitTermination.objects.all(),
        label='Side',
        display_field='term_side',
        disabled_indicator='cable',
        query_params={
            'circuit_id': '$termination_a_circuit'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device',
            'kind': 'physical',
        }
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_provider', 'termination_a_site', 'termination_a_circuit', 'termination_a_id',
            'termination_b_site', 'termination_b_rack', 'termination_b_device', 'termination_b_id'
        ]


class ConnectCircuitTerminationForm(BootstrapMixin, forms.ModelForm):
    termination_a_provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='Provider',
        required=False
    )
    termination_a_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_a_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        label='Circuit',
        display_field='cid',
        query_params={
            'provider_id': '$termination_a_provider',
            'site_id': '$termination_a_site',
        }
    )
    termination_a_id = DynamicModelChoiceField(
        queryset=CircuitTermination.objects.all(),
        label='Side',
        display_field='term_side',
        disabled_indicator='cable',
        query_params={
            'circuit_id': '$termination_a_circuit'
        }
    )
    termination_b_provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='Provider',
        required=False
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_b_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        label='Circuit',
        display_field='cid',
        query_params={
            'provider_id': '$termination_b_provider',
            'site_id': '$termination_b_site',
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=CircuitTermination.objects.all(),
        label='Side',
        display_field='term_side',
        disabled_indicator='cable',
        query_params={
            'circuit_id': '$termination_b_circuit'
        }
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_provider', 'termination_a_site', 'termination_a_circuit', 'termination_a_id',
            'termination_b_provider', 'termination_b_site', 'termination_b_circuit', 'termination_b_id', 'type',
            'status', 'label', 'color', 'length', 'length_unit',
        ]

    def clean_termination_a_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_a_id'], 'pk', None)

    def clean_termination_b_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_b_id'], 'pk', None)


class ConnectFrontPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectFrontPortToRearPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectRearPortForm(ConnectCableToDeviceForm):
    termination_a_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_a_device'
        }
    )
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCircuitTerminationToForm(BootstrapMixin, forms.ModelForm):
    termination_a_provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='Provider',
        required=False
    )
    termination_a_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_a_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        label='Circuit',
        display_field='cid',
        query_params={
            'provider_id': '$termination_a_provider',
            'site_id': '$termination_a_site',
        }
    )
    termination_a_id = DynamicModelChoiceField(
        queryset=CircuitTermination.objects.all(),
        label='Side',
        display_field='term_side',
        disabled_indicator='cable',
        query_params={
            'circuit_id': '$termination_a_circuit'
        }
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False
    )
    termination_b_rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        label='Rack',
        required=False,
        display_field='display_name',
        null_option='None',
        query_params={
            'site_id': '$termination_b_site'
        }
    )
    termination_b_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label='Device',
        required=False,
        display_field='display_name',
        query_params={
            'site_id': '$termination_b_site',
            'rack_id': '$termination_b_rack',
        }
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_provider', 'termination_a_site', 'termination_a_circuit', 'termination_a_id',
            'termination_b_site', 'termination_b_rack', 'termination_b_device', 'termination_b_id'
        ]

    def clean_termination_a_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_a_id'], 'pk', None)

    def clean_termination_b_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_b_id'], 'pk', None)


class ConnectCircuitTerminationToFrontPortForm(ConnectCircuitTerminationToForm):
    termination_b_id = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCircuitTerminationToRearPortForm(ConnectCircuitTerminationToForm):
    termination_b_id = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='cable',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class CableTemplateForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = CableTemplate
        fields = (
            'cable_number', 'type', 'label', 'color', 'length', 'length_unit',
        )


class CableTemplateFilterForm(BootstrapMixin, forms.Form):
    model = CableTemplate
    q = forms.CharField(
        required=False,
        label='Search'
    )
    cable_number = forms.CharField(required=False)
    type = forms.MultipleChoiceField(
        choices=add_blank_choice(CableTypeChoices),
        required=False,
        widget=StaticSelect2()
    )
    color = forms.CharField(
        max_length=6,  # RGB color code
        required=False,
        widget=ColorSelect()
    )


class CommissionForm(BootstrapMixin, forms.Form):
    cable = forms.ModelChoiceField(
        queryset=Cable.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput()
    )
    template = forms.CharField(
        required=False,
    )

    def clean(self):
        super().clean()
        try:
            if CableTemplate.objects.get(cable_number=self.cleaned_data['template']).cable is not None:
                raise forms.ValidationError({"template": "the assigned cable template is already in use"})
        except ObjectDoesNotExist:
                raise forms.ValidationError({"template": "the assigned cable template does not exist"})

    def save(self):

        template = CableTemplate.objects.get(cable_number=self.cleaned_data['template'])
        cable = self.cleaned_data['cable']

        for field in ['type', 'label', 'color', 'length', 'length_unit']:
            value = getattr(template, field)
            if value:
                setattr(cable, field, value)

        if not template.label:
            cable.label = template.cable_number

        connected_status = None
        statuses = Status.objects.get_for_model(Cable)

        for status in statuses:
            if status.slug == CableStatusChoices.STATUS_CONNECTED:
                connected_status = status

        cable.status = connected_status
        cable.save()
        template.cable = cable
        template.save()

        return cable

class UndoCommissionForm(BootstrapMixin, forms.Form):

    def save(self):
        cable = self.cleaned_data['cable']

        for field in ['type', 'label', 'color', 'length', 'length_unit']:
            value = getattr(template, field)
            if value:
                setattr(cable, field, value)

        connected_status = None
        statuses = Status.objects.get_for_model(Cable)

        for status in statuses:
            if status.slug == CableStatusChoices.STATUS_CONNECTED:
                connected_status = status

        cable.status = connected_status
        cable.save()

        return cable


class CableTemplateCSVForm(CSVModelForm):
    class Meta:
        model = CableTemplate
        fields = CableTemplate.csv_headers


class MeasurementLogForm(BootstrapMixin, forms.ModelForm):
    cable = DynamicModelChoiceField(
        queryset=Cable.objects.all(),
        display_field='label'
    )

    class Meta:
        model = MeasurementLog
        fields = ('link', 'cable')
