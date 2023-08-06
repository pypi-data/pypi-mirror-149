from coldcms.blocks import blocks
from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtailyoast.edit_handlers import YoastPanel


class FAQPage(ColdCMSPageMixin, Page):
    """FAQ model."""

    content = RichTextField(blank=True, default="", verbose_name=_("Content"))
    questions_groups = StreamField(
        [("questions_groups", blocks.QuestionCategoryBlock())],
        blank=True,
        null=True,
        verbose_name=_("Question groups"),
    )

    template = "faq/faq.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("content"),
        StreamFieldPanel("questions_groups"),
    ]

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
        verbose_name = _("FAQ Page")
