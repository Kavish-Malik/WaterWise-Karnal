from django import template

register = template.Library()

@register.filter
def is_not_safe(data_list):
    return any(getattr(d, 'status', None) != 'Safe' for d in data_list)
