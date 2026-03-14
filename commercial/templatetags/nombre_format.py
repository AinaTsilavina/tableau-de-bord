from django import template

register = template.Library()

@register.filter
def separateur_millier(value):
    try:
        value = float(value)
        return '{:,.0f}'.format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value
