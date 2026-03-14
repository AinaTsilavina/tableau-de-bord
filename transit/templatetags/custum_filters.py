from django import template
register = template.Library()

@register.filter
def currency(value, devise):
    try:
        if (devise == "EUR"):
            return "{: .2f} €".format(value)
        elif (devise == "USD"):
            return "$ {: .2f}".format(value).replace(",", " ").replace(".", ",")
    except (ValueError, TypeError):
        return value
