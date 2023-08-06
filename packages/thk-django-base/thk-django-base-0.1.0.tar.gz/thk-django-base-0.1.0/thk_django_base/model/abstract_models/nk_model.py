# -*- coding: utf-8 -*-
from django.db import models
from thk_django_base.inward.natural_key.natural_key_generator import nkg

from .type_hint_model import TypeHintModel


class NKModel(TypeHintModel):
    id = models.BigIntegerField('id', primary_key=True, default=nkg.generate_nk)

    class Meta:
        abstract = True
