from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import View

from nautobot.dcim.models import RearPort, Cable, CablePath, Device, Rack
from nautobot.core.views.generic import (
    BulkDeleteView, BulkImportView, GetReturnURLMixin, ObjectEditView,
    ObjectListView
)
from nautobot.utilities.forms import ConfirmationForm
from nautobot.extras.models.statuses import Status

import time

from . import filters, forms, tables
from .models import CableTemplate, MeasurementLog


class ReconnectView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = 'dcim.add_cable'
    template_name = 'nautobot_cable_utils/cable_connect.html'

    def dispatch(self, request, *args, pk=None, **kwargs):
        self.obj = Cable.objects.get(pk=pk)

        idx = (self.obj.termination_a_type.model, self.obj.termination_b_type.model)
        idx_sorted = tuple(sorted(idx))
        if idx != idx_sorted:
            termination_a = self.obj.termination_a
            self.obj.termination_a = self.obj.termination_b
            self.obj.termination_b = termination_a

        self.form_class = {
            ('circuittermination', 'circuittermination'): forms.ConnectCircuitTerminationForm,
            ('circuittermination', 'rearport'): forms.ConnectCircuitTerminationToRearPortForm,
            ('consoleport', 'consoleserverport'): forms.ConnectConsolePortToConsoleServerPortForm,
            ('consoleport', 'frontport'): forms.ConnectConsolePortToFrontPortForm,
            ('consoleport', 'rearport'): forms.ConnectConsolePortToRearPortForm,
            ('consoleserverport', 'frontport'): forms.ConnectConsoleServerPortToFrontPortForm,
            ('consoleserverport', 'rearport'): forms.ConnectConsoleServerPortToRearPortForm,
            ('powerfeed', 'powerport'): forms.ConnectPowerfeedToPowerPortForm,
            ('poweroutlet', 'powerport'): forms.ConnectPowerOutletToPowerPortForm,
            ('circuittermination', 'interface'): forms.ConnectCircuitTerminationToInterfaceForm,
            ('frontport', 'interface'): forms.ConnectFrontPortToInterfaceForm,
            ('interface', 'rearport'): forms.ConnectInterfaceToRearPortForm,
            ('interface', 'interface'): forms.ConnectInterfaceForm,
            ('frontport', 'frontport'): forms.ConnectFrontPortForm,
            ('frontport', 'rearport'): forms.ConnectFrontPortToRearPortForm,
            ('circuittermination', 'frontport'): forms.ConnectCircuitTerminationToFrontPortForm,
            ('rearport', 'rearport'): forms.ConnectRearPortForm,
        }[idx_sorted]

        return super().dispatch(request, *args, **kwargs)

    def prefill_form(self, initial_data, termination):
        o = getattr(self.obj, termination)
        if o and hasattr(o, 'device'):
            device = o.device
            initial_data['{}_device'.format(termination)] = device
            if device.site:
                initial_data['{}_site'.format(termination)] = device.site
            if device.rack:
                initial_data['{}_rack'.format(termination)] = device.rack

    def get(self, request, *args, **kwargs):
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}

        self.prefill_form(initial_data, 'termination_a')
        self.prefill_form(initial_data, 'termination_b')

        form = self.form_class(instance=self.obj, initial=initial_data)

        return render(request, self.template_name, {
            'obj': self.obj,
            'obj_type': Cable._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, self.obj),
        })

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                if hasattr(self.obj.termination_a, '_path') and self.obj.termination_a._path_id:
                    self.obj.termination_a._path = None
            except CablePath.DoesNotExist:
                pass
            try:
                if hasattr(self.obj.termination_b, '_path') and self.obj.termination_b._path_id:
                    self.obj.termination_b._path = None
            except CablePath.DoesNotExist:
                pass
            self.obj.delete()
            self.obj.pk = None
            self.obj._state.adding = True

            self.obj.termination_a.cable = None
            self.obj.termination_b.cable = None

            form = self.form_class(request.POST, request.FILES, instance=self.obj)
            if form.is_valid():
                obj = form.save()

                redirect_url = self.get_return_url(request, obj)
                return redirect(redirect_url)

            return render(request, self.template_name, {
                'obj': self.obj,
                'obj_type': Cable._meta.verbose_name,
                'form': form,
                'return_url': self.get_return_url(request, self.obj),
            })


class CommissionView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = 'dcim.edit_cable'
    template_name = 'nautobot_cable_utils/commission_cable.html'

    def get(self, request, pk=None):
        cable = get_object_or_404(Cable, pk=pk)
        form = forms.CommissionForm(initial={'cable': cable})

        return render(request, self.template_name, {
            'form': form,
            'cable': cable,
            'return_url': self.get_return_url(request, cable),
        })

    def post(self, request, pk=None):
        with transaction.atomic():
            cable = get_object_or_404(Cable, pk=pk)
            form = forms.CommissionForm(request.POST, initial={'cable': cable})

            if form.is_valid():
                form.save()

                return redirect(self.get_return_url(request, cable))

            return render(request, self.template_name, {
                'form': form,
                'cable': cable,
                'return_url': self.get_return_url(request, cable),
            })

class UndoCommissionView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = 'dcim.edit_cable'
    queryset = Cable.objects.all()
    template_name = 'nautobot_cable_utils/undo_commission.html'

    def get(self, request, pk=None):
        cable = get_object_or_404(Cable, pk=pk)
        form = ConfirmationForm(initial=request.GET)

        return render(
            request,
            self.template_name,
            {
                "obj": cable,
                "form": form,
                "obj_type": self.queryset.model._meta.verbose_name,
                "return_url": self.get_return_url(request, cable),
            },
        )

    def post(self, request, pk=None):
        cable = get_object_or_404(Cable, pk=pk)
        form = ConfirmationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                cable_new = Cable()
                cable_new.termination_a = cable.termination_a
                cable_new.termination_b = cable.termination_b
                cable_new.status = Status.objects.get(slug="planned")

                cable.delete()
                cable_new.save()

        return redirect(self.get_return_url(request, cable_new))

class DeviceCommissionView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = 'dcim.edit_cable'
    template_name = 'nautobot_cable_utils/bulk_commission.html'

    def get(self, request, pk=None):
        device = get_object_or_404(Device, pk=pk)

        # set key, if not present
        if 'current_device' not in request.session:
            request.session['current_device'] = None
        
        if request.session['current_device'] != str(pk):
            cable_list = list()
            for cable in device.get_cables().filter(status__slug="planned"):
                cable_list.append(str(cable.pk))

            request.session['current_device'] = str(pk)
            request.session['cable_list'] = cable_list
            request.session.modified = True

        cable = get_object_or_404(Cable, pk=request.session['cable_list'][0])
        form = forms.CommissionForm(initial={'cable': cable})

        return render(request, self.template_name, {
            'form': form,
            'count': len(request.session['cable_list']),
            'object': cable,
            'return_url': self.get_return_url(request, device)
        })

    def post(self, request, pk=None):
        with transaction.atomic():
            device = get_object_or_404(Device, pk=pk)
            cable = get_object_or_404(Cable, pk=request.session['cable_list'][0])
            form = forms.CommissionForm(request.POST, initial={'cable': cable})    
            
            if '_create' in self.request.POST:
                if form.is_valid():
                    request.session['cable_list'].pop(0)
                    request.session.modified = True
                    form.save()
            elif '_skip' in self.request.POST:
                request.session['cable_list'].pop(0)
                request.session.modified = True

            if len(request.session['cable_list']) > 0 and '_cancel' not in self.request.POST:
                if form.is_valid() or '_skip' in self.request.POST:
                    return redirect(request.path)
                else:
                    #re-render page to display ValidationErrors
                    return render(request, self.template_name, {
                        'form': form,
                        'count': len(request.session['cable_list']),
                        'object': get_object_or_404(Cable, pk=request.session['cable_list'][0]),
                        'return_url': self.get_return_url(request, device)
                    })
            
            if 'current_device' in self.request.session.keys():
                del request.session['current_device']
            if 'cable_list' in self.request.session.keys():
                del request.session['cable_list']   
        
        return redirect(self.get_return_url(request, device))


class CableTemplateListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'dcim.view_cable_template'
    queryset = CableTemplate.objects.all()
    filterset = filters.CableTemplateFilterSet
    filterset_form = forms.CableTemplateFilterForm
    table = tables.CableTemplateTable
    action_buttons = tuple()
    template_name = 'nautobot_cable_utils/cable_template_list.html'


class CableTemplateCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'dcim.add_cable_template'
    queryset = CableTemplate.objects.all()
    model_form = forms.CableTemplateForm
    default_return_url = 'plugins:nautobot_cable_utils:cabletemplate_list'


class CableTemplateEditView(CableTemplateCreateView):
    permission_required = 'dcim.edit_cable_template'


class CableTemplateBulkImportView(BulkImportView):
    queryset = CableTemplate.objects.all()
    model_form = forms.CableTemplateCSVForm
    table = tables.CableTemplateTable


class CableTemplateBulkDeleteView(BulkDeleteView):
    queryset = CableTemplate.objects.all()
    filterset = filters.CableTemplateFilterSet
    table = tables.CableTemplateTable


class MeasurementLogListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'dcim.view_measurement_log'
    queryset = MeasurementLog.objects.all()
    table = tables.MeasurementLogTable
    action_buttons = tuple()
    template_name = 'nautobot_cable_utils/measurement_log_list.html'


class MeasurementLogCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'dcim.add_measurement_log'
    queryset = MeasurementLog.objects.all()
    model_form = forms.MeasurementLogForm
    default_return_url = 'plugins:nautobot_cable_utils:measurement_log_list'


class MeasurementLogEditView(CableTemplateCreateView):
    permission_required = 'dcim.edit_measurement_log'


class MeasurementLogBulkDeleteView(BulkDeleteView):
    queryset = MeasurementLog.objects.all()
    table = tables.MeasurementLogTable
