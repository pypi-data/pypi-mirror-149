from coldcms.wagtail_customization.admin_views import generate_statics
from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.core import hooks


@hooks.register("register_admin_urls")
def hook_generate_statics():
    return [
        path(
            "generate_statics/<int:page_id>/",
            generate_statics,
            name="generate_statics",
        )
    ]


@hooks.register("register_page_listing_more_buttons")
def register_button_regenerate_statics(page, page_perms, is_parent=False, next_url=None):
    yield wagtailadmin_widgets.Button(
        _("Re-build page"),
        reverse("generate_statics", kwargs={"page_id": page.pk}),
        priority=60,
    )


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/coldcms_admin.css')
    )


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/coldcms_admin.js')
    )
