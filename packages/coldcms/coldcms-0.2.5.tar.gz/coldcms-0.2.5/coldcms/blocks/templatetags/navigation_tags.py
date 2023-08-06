import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context["request"].site.root_page


@register.inclusion_tag("components/menu/top_menu.html", takes_context=True)
def top_menu(context, parent, first_level=False):
    if not context:
        context = {}
    menuitems = parent.get_children().live().in_menu()
    items = []
    for menuitem in menuitems:
        real_page = menuitem.specific
        real_page.show_dropdown = (
            first_level and len(real_page.get_children().live().in_menu()) > 0
        )
        items.append(real_page)
    return {
        "menuitems": items,
        "context": context,
        "self": context.get("self"),
    }
