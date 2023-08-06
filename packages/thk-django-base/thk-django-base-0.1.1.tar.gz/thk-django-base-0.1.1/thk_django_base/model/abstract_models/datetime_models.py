# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .type_hint_model import TypeHintModel


class CUTimeModel(TypeHintModel):
    created_time: datetime = models.DateTimeField(_("created time"), db_index=True, auto_now_add=True)
    updated_time: datetime = models.DateTimeField(_("updated time"), db_index=True, auto_now=True)

    class Meta:
        abstract = True


class ExpirationModel(TypeHintModel):
    expiration: datetime = models.DateTimeField(_("expiration"), db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def remove_expired(cls):
        cls.objects.filter(expiration__lte=timezone.now()).delete()

    def set_expiry(self, delta: timedelta):
        self.expiration = timezone.now() + delta


class DateRangeModel(TypeHintModel):
    first_date: date = models.DateField(_("first date"), db_index=True)
    last_date: date = models.DateField(_("last date"), db_index=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.first_date > self.last_date:
            raise ValidationError({'first_date': _('First date is greater than the last date.')})
