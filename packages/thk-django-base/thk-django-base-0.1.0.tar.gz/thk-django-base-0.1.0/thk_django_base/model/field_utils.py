# -*- coding: utf-8 -*-
import os

from django.utils.deconstruct import deconstructible


@deconstructible
class PathWithIDName(object):

    def __init__(self, path: str):
        """Use instance id as filename

        Args:
            path: relative path

        """
        self.path = path

    def __call__(self, instance, raw_filename):
        _, ext = os.path.splitext(raw_filename)
        return os.path.join(self.path, str(instance.pk) + ext)
