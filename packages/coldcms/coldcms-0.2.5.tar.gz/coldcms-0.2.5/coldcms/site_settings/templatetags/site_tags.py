from coldcms.site_settings.models import Footer, MenuOptions
from django import template

register = template.Library()


@register.simple_tag
def get_footer_columns():
    try:
        footer = Footer.objects.first()
        return footer.columns.all()
    except Exception:
        return []


@register.simple_tag
def get_footer_icons():
    try:
        footer = Footer.objects.first()
        return footer.icons.stream_data
    except Exception:
        return []


@register.simple_tag
def get_menu_links_icons():
    try:
        menu_options = MenuOptions.objects.first()
        return menu_options.custom_menu_items.stream_data
    except Exception:
        return []
