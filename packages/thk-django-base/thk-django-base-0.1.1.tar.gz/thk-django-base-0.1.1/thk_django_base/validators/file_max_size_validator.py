# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class FileMaxSizeValidator(object):

    def __init__(self, max_size_kb: int):
        self.max_size_kb = max_size_kb

    def __call__(self, data: FieldFile):
        if data.size > self.max_size_kb * 1024:
            raise ValidationError(_("Maximum file limit is {max_size}KB.").format(
                max_size=self.max_size_kb
            ))
