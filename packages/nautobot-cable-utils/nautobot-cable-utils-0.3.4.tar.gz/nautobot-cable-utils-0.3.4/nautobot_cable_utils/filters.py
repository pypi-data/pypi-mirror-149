import django_filters
from django.db.models import Q

from nautobot.utilities.choices import ColorChoices
from nautobot.utilities.filters import BaseFilterSet

from .models import CableTemplate


class CableTemplateFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    color = django_filters.MultipleChoiceFilter(
        choices=ColorChoices
    )

    class Meta:
        model = CableTemplate
        fields = ['cable_number', 'type', 'color']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(cable_number__icontains=value) |
            Q(label__icontains=value)
        )
        return queryset.filter(qs_filter)
