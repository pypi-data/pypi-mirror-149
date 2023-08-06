from coldcms.blocks.blocks import CTABlock
from colorfield.fields import ColorField
from colorfield.widgets import ColorWidget
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    StructBlock,
    URLBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class SocialMediaIconBlock(StructBlock):
    icons_list = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("github", "GitHub"),
        ("gitlab", "GitLab"),
        ("linkedin", "LinkedIn"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("pinterest", "Pinterest"),
        ("tumblr", "Tumblr"),
    ]
    icon_type = ChoiceBlock(
        label=_("Icon type"),
        icon="site",
        blank=False,
        default=icons_list[0],
        choices=icons_list,
        help_text=_(
            "Which social media is the URL linking to (will display the corresponding icon)"
        ),
    )
    link = URLBlock(
        label=_("Link"), icon="link", help_text=_("URL to your social media")
    )
    link_text = CharBlock(
        label=_("Link text"),
        required=False,
        max_length=40,
        help_text=_(
            'The text displayed next to the social media icon. Should be of the type "Follow us on ...". Be aware that some social media companies require that this text appears next to their logo. Make sure by checking their branding website.'
        ),
    )
    blank = BooleanBlock(required=False, label=_("Open link in a new tab"))

    class Meta:
        icon = "site"
        verbose_name = _("Social media icon")
        label = _("Social media icon")


class LinkBlock(StructBlock):
    link = URLBlock(
        label=_("Link"), icon="link", help_text=_("URL")
    )
    link_text = CharBlock(
        label=_("Link text"),
        required=False,
        max_length=40,
    )

    class Meta:
        icon = "anchor"
        verbose_name = _("Link")
        label = _("Link")


@register_setting(icon="code")
class Footer(BaseSetting, ClusterableModel):
    """A footer containing a list of footer columns"""

    icons = StreamField(
        [("social_media_icon", SocialMediaIconBlock())],
        blank=True,
        null=True,
        verbose_name=_("Social media icons"),
    )

    panels = [
        MultiFieldPanel(
            [
                InlinePanel("columns", label=_("Footer columns")),
            ],
            heading=_("Footer columns"),
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("icons"),
            ],
            heading=_("Social media icons"),
            classname="collapsible collapsed",
        ),
    ]

    def __str__(self):
        return "Footer"

    class Meta:
        verbose_name_plural = _("Footer")
        verbose_name = _("Footer")


class FooterColumn(Orderable):
    footer = ParentalKey("site_settings.Footer", related_name="columns")
    title = models.CharField(
        max_length=40, verbose_name=_("Title"), blank=True, null=True
    )
    links = StreamField(
        [("links", CTABlock(icon="link"))],
        blank=True,
        null=True,
        verbose_name=_("Links"),
    )

    panels = [FieldPanel("title"), StreamFieldPanel("links")]


@register_setting(icon="image")
class SiteSettings(BaseSetting):
    """Site settings"""

    LOGO_TYPES = [
        ("image", "JPG, PNG, WEBP, GIF"),
        ("svg", "SVG"),
    ]

    logo_type = models.CharField(
        choices=LOGO_TYPES, max_length=5, default="image", verbose_name=_("Logo type")
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Image"),
    )
    svg = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("SVG"),
    )

    second_logo_type = models.CharField(
        choices=LOGO_TYPES, max_length=5, default="image", verbose_name=_("Second Logo type")
    )
    second_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Image"),
    )
    second_svg = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("SVG"),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "logo_type",
                    classname=(
                        "coldcms-admin__choice-handler "
                        "coldcms-admin__choice-handler--image_type"
                    ),
                ),
                ImageChooserPanel(
                    "image",
                    classname=(
                        "coldcms-admin__choice-handler-target--image_type "
                        "coldcms-admin__choice-handler-hidden-if--svg"
                    ),
                ),
                DocumentChooserPanel(
                    "svg",
                    classname=(
                        "coldcms-admin__choice-handler-target--image_type "
                        "coldcms-admin__choice-handler-hidden-if--image"
                    ),
                ),
            ],
            heading=_("Logo"),
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "second_logo_type",
                    classname=(
                        "coldcms-admin__choice-handler "
                        "coldcms-admin__choice-handler--image_type"
                    ),
                ),
                ImageChooserPanel(
                    "second_image",
                    classname=(
                        "coldcms-admin__choice-handler-target--image_type "
                        "coldcms-admin__choice-handler-hidden-if--svg"
                    ),
                ),
                DocumentChooserPanel(
                    "second_svg",
                    classname=(
                        "coldcms-admin__choice-handler-target--image_type "
                        "coldcms-admin__choice-handler-hidden-if--image"
                    ),
                ),
            ],
            heading=_("Second Logo"),
        )
    ]

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")


@register_setting(icon="doc-full-inverse")
class CSSStyleSheet(BaseSetting):
    """Load a CSS stylesheet"""

    CSS_stylesheet = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        help_text=_(
            "Upload your own CSS stylesheet to custom the appearance of your website"
        ),
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("CSS"),
    )

    panels = [DocumentChooserPanel("CSS_stylesheet")]

    class Meta:
        verbose_name = _("CSS stylesheet")
        verbose_name_plural = _("CSS stylesheets")


@register_setting(icon="collapse-down")
class MenuOptions(BaseSetting):
    """Option to show or hide the menu bar"""

    hide_menu = models.BooleanField(
        verbose_name=_("Hide Menu"),
        default=False,
        help_text=_("Whether to hide the menu bar or not"),
    )

    custom_menu_items = StreamField(
        [
            ("social_media_icon", SocialMediaIconBlock()),
            ("link", LinkBlock()),
        ],
        blank=True,
        null=True,
        verbose_name=_("Links and social media icons"),
    )

    panels = [
        FieldPanel("hide_menu"),
        MultiFieldPanel(
            [StreamFieldPanel("custom_menu_items"), ],
            heading=_("Links and social media icons"),
        ),
    ]

    class Meta:
        verbose_name = _("Menu options")


@register_setting(icon="edit")
class VariablesColors(BaseSetting):

    black = ColorField(default=settings.BLACK, verbose_name=_("Black"))
    black_bis = ColorField(default=settings.BLACK_BIS, verbose_name=_("Black bis"))
    black_ter = ColorField(
        default=settings.BLACK_TER, verbose_name=_("Black ter")
    )

    grey_darker = ColorField(
        default=settings.GREY_DARKER, verbose_name=_("grey darker")
    )
    grey_dark = ColorField(default=settings.GREY_DARK, verbose_name=_("Grey dark"))
    grey = ColorField(default=settings.GREY, verbose_name=_("Grey"))
    grey_light = ColorField(default=settings.GREY_LIGHT, verbose_name=_("Grey light"))
    grey_lighter = ColorField(
        default=settings.GREY_LIGHTER, verbose_name=_("Grey lighter")
    )
    grey_lightest = ColorField(
        default=settings.GREY_LIGHTEST, verbose_name=_("Grey lightest")
    )

    white = ColorField(default=settings.WHITE, verbose_name=_("White"))
    white_bis = ColorField(default=settings.WHITE_BIS, verbose_name=_("White bis"))
    white_ter = ColorField(
        default=settings.WHITE_TER, verbose_name=_("White ter")
    )

    orange = ColorField(default=settings.ORANGE, verbose_name=_("Orange"))
    yellow = ColorField(default=settings.YELLOW, verbose_name=_("Yellow"))
    green = ColorField(default=settings.GREEN, verbose_name=_("Green"))
    turquoise = ColorField(default=settings.TURQUOISE, verbose_name=_("Turquoise"))
    cyan = ColorField(default=settings.CYAN, verbose_name=_("Cyan"))
    blue = ColorField(default=settings.BLUE, verbose_name=_("Blue"))
    purple = ColorField(default=settings.PURPLE, verbose_name=_("Purple"))
    red = ColorField(default=settings.RED, verbose_name=_("Red"))

    primary = ColorField(default=settings.PRIMARY, verbose_name=_("Primary"))
    info = ColorField(default=settings.INFO, verbose_name=_("Info"))
    success = ColorField(default=settings.SUCCESS, verbose_name=_("Success"))
    warning = ColorField(default=settings.WARNING, verbose_name=_("Warning"))
    danger = ColorField(default=settings.DANGER, verbose_name=_("Danger"))

    panels = [
        FieldPanel("black", widget=ColorWidget),
        FieldPanel("black_bis", widget=ColorWidget),
        FieldPanel("black_ter", widget=ColorWidget),
        FieldPanel("grey_darker", widget=ColorWidget),
        FieldPanel("grey_dark", widget=ColorWidget),
        FieldPanel("grey", widget=ColorWidget),
        FieldPanel("grey_light", widget=ColorWidget),
        FieldPanel("grey_lighter", widget=ColorWidget),
        FieldPanel("grey_lightest", widget=ColorWidget),
        FieldPanel("white_ter", widget=ColorWidget),
        FieldPanel("white_bis", widget=ColorWidget),
        FieldPanel("white", widget=ColorWidget),
        FieldPanel("orange", widget=ColorWidget),
        FieldPanel("yellow", widget=ColorWidget),
        FieldPanel("green", widget=ColorWidget),
        FieldPanel("turquoise", widget=ColorWidget),
        FieldPanel("cyan", widget=ColorWidget),
        FieldPanel("blue", widget=ColorWidget),
        FieldPanel("purple", widget=ColorWidget),
        FieldPanel("red", widget=ColorWidget),
        FieldPanel("primary", widget=ColorWidget),
        FieldPanel("info", widget=ColorWidget),
        FieldPanel("success", widget=ColorWidget),
        FieldPanel("warning", widget=ColorWidget),
        FieldPanel("danger", widget=ColorWidget),
    ]

    class Meta:
        verbose_name = _("Colors")
