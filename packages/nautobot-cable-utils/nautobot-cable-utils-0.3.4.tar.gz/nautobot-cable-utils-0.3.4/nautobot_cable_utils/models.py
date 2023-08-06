from django.db import models

from nautobot.dcim.choices import *
from nautobot.dcim.models import Cable
from nautobot.utilities.fields import ColorField
from nautobot.utilities.querysets import RestrictedQuerySet
from nautobot.core.models import BaseModel


class CableTemplate(BaseModel):
    cable_number = models.CharField(
        max_length=50,
        unique=True,
    )
    type = models.CharField(
        max_length=50,
        choices=CableTypeChoices,
        blank=True
    )
    label = models.CharField(
        max_length=100,
        blank=True
    )
    color = ColorField(
        blank=True
    )
    length = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    length_unit = models.CharField(
        max_length=50,
        choices=CableLengthUnitChoices,
        blank=True,
    )
    cable = models.OneToOneField(
        Cable,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = RestrictedQuerySet.as_manager()

    csv_headers = [
        'cable_number', 'type', 'label', 'color', 'length', 'length_unit',
    ]

    def __str__(self):
        return self.cable_number


class MeasurementLog(BaseModel):
    link = models.URLField(
        blank=True,
        null=True
    )
    cable = models.OneToOneField(
        Cable,
        on_delete=models.CASCADE,
    )
