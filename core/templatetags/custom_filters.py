from django import template

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list."""
    return value.split(delimiter)


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    return dictionary.get(key)


@register.filter
def subtract(value, arg):
    """Subtract arg from value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """Calculate percentage."""
    try:
        return round((int(value) / int(total)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
