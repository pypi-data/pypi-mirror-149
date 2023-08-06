from django.template.defaulttags import register


@register.filter
def index(items, i):
    return items[i]
