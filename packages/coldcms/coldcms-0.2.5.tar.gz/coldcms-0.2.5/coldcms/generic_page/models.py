from coldcms.blocks.blocks import (
    ColoredBlock,
    CTABlock,
    FormBlock,
    HeaderBlock,
    ImageBlock,
    ImageUrlBlock,
    LogoBlock,
    QuestionCategoryBlock,
    QuoteBlock,
)
from coldcms.blog.blocks import BlogListBlock
from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtailyoast.edit_handlers import YoastPanel


class GenericCarouselSlide(StructBlock):
    """A slide within a carousel"""

    title = CharBlock(required=False, max_length=100, label=_("Title"))
    text = TextBlock(required=False, max_length=250, label=_("Slide text"))
    buttons = ListBlock(CTABlock(icon="link"), label=_("Buttons"))
    image = ImageBlock(required=True)

    class Meta:
        icon = "image"
        label = _("Carousel slide")


class GenericCarouselBlock(StructBlock):
    """A block with an optional title and a list of slides"""

    title = CharBlock(required=False, max_length=100, label=_("Title (optional)"))
    slides = ListBlock(
        GenericCarouselSlide(),
        icon="image",
        label=_("Carousel"),
    )

    class Meta:
        icon = "image"
        label = _("Carousel")


class GenericCard(ColoredBlock):
    """ A card """

    title = CharBlock(required=False, max_length=250, label=_("Title"))
    text = RichTextBlock(
        required=False,
        features=[
            "bold",
            "italic",
            "link",
            "document-link",
            "ol",
            "ul",
            "hr",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ],
        label=_("Text"),
    )
    image = ImageBlock(required=False)
    buttons = ListBlock(CTABlock(icon="link"), label=_("Buttons"))

    class Meta:
        icon = "form"
        label = _("Card")


class GenericBigCard(GenericCard):
    position_image = ChoiceBlock(choices=[
        ('left', _("Left")),
        ('right', _("Right")),
    ], icon='cup', label=_("Image position"), required=False)

    class Meta:
        icon = "form"
        label = _("Big card")


class ContainerGenericCard(ColoredBlock):
    """ Container card """

    title = CharBlock(required=False, max_length=100, label=_("Title"))
    cards = ListBlock(GenericCard(), label=_("Cards"))

    class Meta:
        icon = "placeholder"
        label = _("Card container")


class ContainerListGenericCard(ContainerGenericCard):
    class Meta:
        icon = "list-ul"
        label = _("List card container")


class GenericTextBlock(ColoredBlock):
    title = CharBlock(required=False, label=_("Title"))
    text = RichTextBlock(
        required=False,
        features=[
            "bold",
            "italic",
            "link",
            "document-link",
            "ol",
            "ul",
            "hr",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ],
        label=_("Text"),
    )
    text_alignment = ChoiceBlock(choices=[
        ('has-text-centered', _("Center")),
        ('has-text-left', _("Left")),
        ('has-text-right', _("Right")),
        ('has-text-justified', _("Justify")),
    ], icon='cup', label=_("Text alignment"))

    buttons = ListBlock(
        CTABlock(icon="link"),
        label=_("Buttons (optional)"),
    )

    class Meta:
        icon = "title"
        label = _("Text Block")


class GenericImage(StructBlock):
    image = ImageBlock(label=_("Image"))
    fullwidth = BooleanBlock(default=False, label=_("Fullwidth"), required=False)
    url = CTABlock(label=_("Image link (optionnaly)"))

    class Meta:
        icon = "image"
        label = _("Generic Image")


class ImageListBlock(StructBlock):
    title = CharBlock(max_length=100, label=_("Title"), required=False)
    list_images = ListBlock(ImageUrlBlock())

    class Meta:
        icon = "image"
        label = _("Image List Block")


GenericStreamField = [
    ("blog_list_block", BlogListBlock(label=_("Section preview articles"))),
    ("header_block", HeaderBlock()),
    ("carousel", GenericCarouselBlock()),
    ("generic_text_block", GenericTextBlock()),
    ("generic_image", GenericImage()),
    ("big_card", GenericBigCard()),
    ("container_card", ContainerGenericCard()),
    ("container_list_card", ContainerListGenericCard()),
    ("form_block", FormBlock()),
    ("logo_block", LogoBlock()),
    ("quote_block", QuoteBlock()),
    ("image_list_block", ImageListBlock()),
    (
        "container_two_blocks",
        StreamBlock(
            [
                ("quote_block", QuoteBlock()),
                ("image_block", ImageUrlBlock()),
                ("form_block", FormBlock()),
                ("generic_text_block", GenericTextBlock()),
            ],
            min_num=2,
            max_num=2,
        ),
    ),
    ("quote_block", QuoteBlock()),
    ("image_list_block", ImageListBlock()),
    ("question_category_block", QuestionCategoryBlock()),
]


class ColumnBlock(StructBlock):
    content = StreamBlock(
        GenericStreamField + [(
            "box_block",
            StreamBlock(GenericStreamField),
        )],
    )

    class Meta:
        icon = "placeholder"
        label = _("Column Block")


class ColumnsBlock(ColoredBlock):
    title = CharBlock(max_length=100, label=_("Title"), required=False)
    columns = ListBlock(
        ColumnBlock(label=_("Column Block")),
        label=_("Columns")
    )

    class Meta:
        icon = "placeholder"
        label = _("Columns Block")


class GenericPage(ColdCMSPageMixin, Page):
    """Generic page model."""

    template = "generic_page/generic_page.html"
    show_in_menus_default = True

    content_blocks = StreamField(
        GenericStreamField
        + [
            (
                "columns_block",
                ColumnsBlock(),
            ),
            (
                "container_three_blocks",
                StreamBlock(
                    [
                        ("quote_block", QuoteBlock()),
                        ("image_block", ImageUrlBlock()),
                        ("form_block", FormBlock()),
                        ("generic_text_block", GenericTextBlock()),
                    ],
                    min_num=3,
                    max_num=3,
                ),
            ),
            (
                "box_block",
                StreamBlock(GenericStreamField),
            )
        ],
        blank=True,
        null=True,
        verbose_name=_("Content"),
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content_blocks"),
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
        verbose_name = _("Generic page")
