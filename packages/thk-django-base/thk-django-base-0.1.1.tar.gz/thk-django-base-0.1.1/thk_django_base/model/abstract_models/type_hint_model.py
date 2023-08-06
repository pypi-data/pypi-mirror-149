# -*- coding: utf-8 -*-
from django.db import models


class TypeHintModel(models.Model):
    objects: models.QuerySet
    id: int

    class Meta:
        abstract = True
