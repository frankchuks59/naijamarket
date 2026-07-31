# marketplace/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.simple_tag
def is_selected(current_value, check_value):
    """Returns 'selected' if values match"""
    if str(current_value) == str(check_value):
        return 'selected'
    return ''

@register.simple_tag
def is_checked(current_value, check_value):
    """Returns 'checked' if values match"""
    if str(current_value) == str(check_value):
        return 'checked'
    return ''