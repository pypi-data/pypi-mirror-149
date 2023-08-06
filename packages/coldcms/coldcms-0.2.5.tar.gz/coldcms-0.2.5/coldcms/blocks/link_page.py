from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    TabbedInterface,
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page


class LinkPageAdminForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].help_text = _(
            "By default, this will be used as the link text when appearing "
            "in menus."
        )


class AbstractLinkPage(Page):
    """Taken and adapted from wagtailmenus"""

    link_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("*OR* Link to an internal page"),
        help_text=_("Ignored if the external URL is used"),
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    link_url = models.CharField(
        verbose_name=_("link to an external URL"),
        max_length=255,
        blank=True,
        null=True,
    )
    url_append = models.CharField(
        verbose_name=_("append to URL"),
        max_length=255,
        blank=True,
        help_text=_(
            "Use this to optionally append a #hash or querystring to the URL."
        ),
    )

    subpage_types = []  # Don't allow subpages
    search_fields = []  # Don't surface these pages in search results
    base_form_class = LinkPageAdminForm

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_menus = True

    def menu_text(self, request=None):
        """Return a string to use as link text when this page appears in
        menus."""
        source_field_name = "title"
        if source_field_name != "menu_text" and hasattr(
            self, source_field_name
        ):
            return getattr(self, source_field_name)
        return self.title

    def clean(self, *args, **kwargs):
        if self.link_page and isinstance(
            self.link_page.specific, AbstractLinkPage
        ):
            raise ValidationError(
                {
                    "link_page": ValidationError(
                        _("A link page cannot link to another link page"),
                        code="invalid",
                    )
                }
            )
        if not self.link_url and not self.link_page:
            raise ValidationError(
                _("Please choose an internal page or provide an external URL"),
                code="invalid",
            )
        if self.link_url and self.link_page:
            raise ValidationError(
                _("Linking to both a page and external URL is not permitted"),
                code="invalid",
            )
        super().clean(*args, **kwargs)

    def link_page_is_suitable_for_display(
        self,
        request=None,
        current_site=None,
        menu_instance=None,
        original_menu_tag="",
    ):
        """
        Like menu items, link pages linking to pages should only be included
        in menus when the target page is live and is itself configured to
        appear in menus. Returns a boolean indicating as much
        """
        if self.link_page:
            if (
                not self.link_page.show_in_menus
                or not self.link_page.live
                or self.link_page.expired
            ):
                return False
        return True

    def show_in_menus_custom(
        self,
        request=None,
        current_site=None,
        menu_instance=None,
        original_menu_tag="",
    ):
        """
        Return a boolean indicating whether this page should be included in
        menus being rendered.
        """
        if not self.show_in_menus:
            return False
        if self.link_page:
            return self.link_page_is_suitable_for_display()
        return True

    def get_sitemap_urls(self, request=None):
        return []  # don't include pages of this type in sitemaps

    def _url_base(self, request=None, current_site=None, full_url=False):
        # Return the url of the page being linked to, or the custom URL
        if self.link_url:
            return self.link_url

        if not self.link_page:
            return ""

        p = self.link_page.specific  # for tidier referencing below
        if full_url:
            return p.get_full_url(request=request)
        return p.get_url()

    def get_url(self, request=None, current_site=None):
        try:
            base = self._url_base(request=request, current_site=current_site)
            return base + self.url_append
        except TypeError:
            pass  # self.link_page is not routable
        return ""

    url = property(get_url)

    def get_full_url(self, request=None):
        try:
            base = self._url_base(request=request, full_url=True)
            return base + self.url_append
        except TypeError:
            pass  # self.link_page is not routable
        return ""

    full_url = property(get_full_url)

    def relative_url(self, current_site, request=None):
        return self.get_url(request=request, current_site=current_site)

    def serve(self, request, *args, **kwargs):
        # Display appropriate message if previewing
        if getattr(request, "is_preview", False):
            return HttpResponse(
                _("This page redirects to: %(url)s")
                % {"url": self.get_full_url(request)}
            )
        # Redirect to target URL if served
        site = getattr(request, "site", None)
        return redirect(self.relative_url(current_site=site, request=request))

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    MultiFieldPanel(
                        [
                            FieldPanel("title", classname="title"),
                            FieldPanel("link_url"),
                            PageChooserPanel("link_page"),
                            FieldPanel("url_append"),
                            FieldPanel("show_in_menus"),
                        ]
                    )
                ],
                heading=_("Settings"),
                classname="settings",
            )
        ]
    )
