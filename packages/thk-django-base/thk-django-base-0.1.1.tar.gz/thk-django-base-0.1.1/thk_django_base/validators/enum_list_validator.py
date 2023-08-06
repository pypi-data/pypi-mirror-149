# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class EnumListValidator(object):

    def __init__(self, enum_list: list, need_unique: bool = True):
        self.enum_list = enum_list
        self.need_unique = need_unique

    def __call__(self, value_list: list):
        value_set = set()
        for value in value_list:
            if value not in self.enum_list:
                raise ValidationError(_("Invalid enum: {value}.").format(value=value))
            value_set.add(value)

        if self.need_unique and len(value_set) != len(value_list):
            raise ValidationError(_("Contains duplicate values."))
