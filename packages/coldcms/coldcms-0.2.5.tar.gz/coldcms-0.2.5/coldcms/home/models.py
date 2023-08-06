from coldcms.blocks.blocks import CTABlock
from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.blocks import (
    CharBlock,
    ListBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtailyoast.edit_handlers import YoastPanel


class HomePageCarouselSlide(StructBlock):
    """A slide within a carousel"""

    title = CharBlock(required=False, max_length=60, label=_("Title"))
    text = TextBlock(required=False, max_length=200, label=_("Slide text"))
    buttons = ListBlock(CTABlock(icon="link"), label=_("Buttons"))
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = "image"
        label = _("Carousel slide")


class HomePageCard(StructBlock):
    """ A card """

    title = CharBlock(required=True, max_length=40, label=_("Title"))
    text = RichTextBlock(
        required=False,
        features=["bold", "italic", "link", "document-link", "ol", "ul", "hr"],
        label=_("Text"),
    )
    buttons = ListBlock(CTABlock(icon="link"), label=_("Buttons"))
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "form"
        label = _("Card")


class HomePage(ColdCMSPageMixin, Page):
    """Home page model."""

    template = "home/home_page.html"
    show_in_menus_default = True
    parent_page_types = []

    home_content_blocks = StreamField(
        [
            (
                "carousel",
                ListBlock(HomePageCarouselSlide(), icon="image", label=_("Carousel")),
            ),
            (
                "big_card",
                ListBlock(HomePageCard(), icon="form", label=_("Big cards group")),
            ),
            (
                "small_card",
                ListBlock(HomePageCard(), icon="form", label=_("Small cards group")),
            ),
        ],
        blank=True,
        null=True,
        verbose_name=_("Content"),
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("home_content_blocks"),
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
        verbose_name = _("Home Page")
