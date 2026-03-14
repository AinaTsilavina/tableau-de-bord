from django import template


register = template.Library()

@register.filter
def splitWords(value):
    return value.split()
