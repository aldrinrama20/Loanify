from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    return value.lower().endswith(suffix.lower())