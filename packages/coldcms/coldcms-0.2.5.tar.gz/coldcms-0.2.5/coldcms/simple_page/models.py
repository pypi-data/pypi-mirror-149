from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtailyoast.edit_handlers import YoastPanel


class SimplePage(ColdCMSPageMixin, Page):
    """Simple Page model."""

    subtitle = models.TextField(blank=True, null=True, verbose_name=_("Subtitle"))
    content = RichTextField(verbose_name=_("Content"))

    template = "simple_page/simple_page.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [FieldPanel("content")]

    keywords = models.CharField(default='', blank=True, max_length=100, verbose_name=_("Key words"))
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(
                Page.promote_panels,
                heading=_("Promote"),
                classname="settings",
            ),
            YoastPanel(
                keywords='keywords',
                title='seo_title',
                search_description='search_description',
                slug='slug'
            ),
        ]
    )

    class Meta:
        verbose_name = _("Simple page")
