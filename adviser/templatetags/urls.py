# -*- coding: utf-8 -*-
from typing import Optional, Any, Dict

from django import urls, template

from adviser.models import GeneralFields

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context: Dict[str, Any], language: Optional[str]) -> str:
    """Get the absolute URL of the current page for the specified language.

    Usage:
        {% translate_url 'en' %}
    """
    url = context['request'].build_absolute_uri()
    return urls.translate_url(url, language)


@register.simple_tag()
def get_extra_fields():
    return GeneralFields.objects.first()
