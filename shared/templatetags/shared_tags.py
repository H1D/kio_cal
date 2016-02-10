# -*- coding: utf-8 -*-
import sys
import urllib2
import json
from django.template import Library
from django.core.cache import cache

register = Library()

@register.simple_tag
def inflect(name, case):
    '''
    0 Кто? — Крым
    1 Кого? — Крыма (родительный падеж)
    2 Кому? — Крыму
    3 Кого? — Крыма (винительный падеж)
    4 Кем? — Крымом
    5 О ком? — о Крыме
    '''
    cache_key='inflector_'.join((name,))
    cases = cache.get(cache_key)

    if not cases:
        url = 'http://export.yandex.ru/inflect.xml?name=%s&format=json'\
                                    %urllib2.quote(name.encode('utf-8'))
        try:
            response = urllib2.urlopen(url,timeout=500)
            #FIXME catch exact
        except:
            return name
        cases = json.load(response)
        cache.set(cache_key,cases,3600 * 24 * 365)
    try:
        return cases[str(case)]
    except KeyError:
        return name


def model_verbose_name(obj):
    return obj._meta.verbose_name
register.filter(model_verbose_name)

def display_value(field):
    """
    Returns the displayed value for this BoundField, as rendered in widgets.
    """
    value = field_value(field)

    if isinstance(field.field, ChoiceField):
        return dict((unicode(k), v)
                    for k, v in field.field.choices).get(unicode(value))
    else:
        return value
register.filter(display_value)


@register.filter
def replace ( string, args ):
    #regexp should be simpler, but slow

    # if many replaces
    if ';' in args:
        #replace each
        for arg in args.split(';'):
            if '|' in arg:
                search  = arg.split('|')[0]
                replace = arg.split('|')[1]
                string = string.replace(search,replace)
    else:
        #token are correct?
        if '|' in args:
                search  = arg.split('|')[0]
                replace = arg.split('|')[1]
                string = string.replace(search,replace)
    return string

@register.filter
def has_attr (obj, args ):
    return hasattr(obj,args[0])