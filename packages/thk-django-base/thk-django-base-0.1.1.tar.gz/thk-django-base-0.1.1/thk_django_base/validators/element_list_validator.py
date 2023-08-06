# -*- coding: utf-8 -*-
from typing import Callable
from django.utils.deconstruct import deconstructible


@deconstructible
class ElementListValidator(object):

    def __init__(self, validator: Callable):
        self.validator = validator

    def __call__(self, value_list: list):
        for value in value_list:
            self.validator(value)
