from coldcms.blocks.link_page import AbstractLinkPage
from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.models import Page


class LinkPage(AbstractLinkPage):
    class Meta:
        verbose_name = _("Internal or external link")


class DropDownPage(ColdCMSPageMixin, Page):
    search_fields = []  # Don't surface these pages in search results

    parent_page_types = ["generic_page.GenericPage"]
    url = "#"
    show_in_menus_default = True

    def get_sitemap_urls(self, request=None):
        return []  # don't include pages of this type in sitemaps

    def serve(self, request, *args, **kwargs):
        raise Http404()

    class Meta:
        verbose_name = _("Dropdown")

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    MultiFieldPanel(
                        [
                            FieldPanel("title", classname="title"),
                            FieldPanel("show_in_menus"),
                        ]
                    )
                ],
                heading=_("Settings"),
                classname="settings",
            )
        ]
    )
