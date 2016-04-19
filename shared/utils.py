# -*- coding: utf-8 -*-
import os
import uuid

from django.core.urlresolvers import reverse
from django import db

from django.conf import settings

def define(name, default=None):
    """
    Updates settings module with a given default value for an
    option, if it's not defined already.
    """
    if not hasattr(settings, name):
        return setattr(settings, name, default)

def get_admin_url(obj):
    if obj and db.models.Model in obj.__class__.__bases__ and obj.pk:
        return reverse('admin:%s_%s_change' %
                   (obj._meta.app_label, obj._meta.module_name), args=(obj.pk,))

def upload_to(prefix):
    """
    Helper function, allowing FileField to "randomly" rename uploaded
    files.

    Usage:

        class SomeModel(models.Model):
            ...
            avatar = models.ImageField(upload_to=upload_to("avatars/")
    """
    upload_path = os.path.join(settings.UPLOAD_PATH, prefix)
    upload_path_absolute = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.isdir(upload_path_absolute):
        os.makedirs(upload_path_absolute)
    def inner(instance, filename):
        fname, fext = os.path.splitext(filename)
        path = os.path.join(
            upload_path,
            uuid.uuid1().hex + fext)
        return path
    return inner

def int2roman(number):
    numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
        50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
    result = ""
    for value, numeral in sorted(numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result