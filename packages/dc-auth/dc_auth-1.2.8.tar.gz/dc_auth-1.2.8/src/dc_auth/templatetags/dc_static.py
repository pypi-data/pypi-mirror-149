from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def dc_static(path):
    return settings.DC_STATIC_URL + "/" + path


@register.simple_tag
def dc_static_js(path):
    return settings.DC_STATIC_URL + "/js/" + path


@register.simple_tag
def dc_static_css(path):
    return settings.DC_STATIC_URL + "/css/" + path


@register.simple_tag
def dc_static_img(path):
    return settings.DC_STATIC_URL + "/img/" + path
