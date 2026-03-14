from django import template
from collections import defaultdict

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key, {})


@register.filter
def filter_valid_values(values):
    if not values:
        return[]
    return[val for val in values if val.get("cat") and val.get("temperature")]


@register.filter
def sort_numbers(numbers):
    try:
        return sorted(numbers, key=lambda x: int(x))
    except ValueError:
        return numbers
    
@register.filter
def group_by_category(values):
    grouped = defaultdict(list)
    for val in values:
        grouped[val["cat"]].append(val)
    return dict(grouped)