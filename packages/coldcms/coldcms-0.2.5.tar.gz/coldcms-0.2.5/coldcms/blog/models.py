from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailyoast.edit_handlers import YoastPanel


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(ColdCMSPageMixin, Page):
    date = models.DateField(verbose_name=_("Post date"))
    intro = models.CharField(
        blank=True, default="", max_length=250, verbose_name=_("Intro")
    )
    body = RichTextField(verbose_name=_("Body"))
    tags = ClusterTaggableManager(
        through=BlogPageTag, blank=True, verbose_name=_("Tags")
    )

    search_fields = [index.SearchField("intro"), index.SearchField("body")]
    subpage_types = []
    parent_page_types = ["blog.BlogIndexPage"]
    show_in_menus_default = False

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("date"), FieldPanel("tags")], heading=_("Blog information"),
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label=_("Gallery images")),
    ]
    edit_handler = TabbedInterface([ObjectList(content_panels, heading=_("Content"))])

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["tag_page"] = {
            tag_index.tag: tag_index.url for tag_index in BlogTagIndexPage.objects.all()
        }
        context["author_index"] = BlogAuthorIndexPage.objects.filter(
            author=context["page"].owner
        ).first()
        return context

    class Meta:
        verbose_name = _("Blog Page")


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Image"),
    )
    caption = models.CharField(
        blank=True, max_length=250, default="", verbose_name=_("Caption")
    )

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]


class BlogIndexPage(ColdCMSPageMixin, Page):
    intro = RichTextField(
        blank=True, default="", max_length=500, verbose_name=_("Intro")
    )
    keywords = models.CharField(default='', blank=True, max_length=100, verbose_name=_("Key words"))

    subpage_types = ["blog.BlogPage"]
    show_in_menus_default = True

    content_panels = Page.content_panels + [FieldPanel("intro")]
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blog_pages = (
            BlogPage.objects.child_of(self).live().order_by("-first_published_at")
        )
        context["blog_pages"] = blog_pages
        context["blog_tags"] = BlogTagGroupByBlogPage.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name = "Blog"


class BlogTagIndexPage(ColdCMSPageMixin, Page):
    tag = models.ForeignKey(Tag, related_name="+", on_delete=models.SET_NULL, null=True)

    content_panels = Page.content_panels + [FieldPanel("tag")]
    parent_page_types = []
    template = "blog/index_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["blog_pages"] = (
            BlogPage.objects.filter(tags=self.tag)
            .live()
            .order_by("-first_published_at")
        )
        return context


class BlogTagGroupByBlogPage(ColdCMSPageMixin, Page):
    tag = models.ForeignKey(Tag, related_name="+", on_delete=models.SET_NULL, null=True)

    content_panels = Page.content_panels + [FieldPanel("tag")]
    parent_page_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["blog_pages"] = (
            BlogPage.objects
                    .child_of(self.get_parent())
                    .filter(tags=self.tag)
                    .live()
                    .order_by("-first_published_at")
        )
        context["blog_tags"] = BlogTagGroupByBlogPage.objects.child_of(self.get_parent())
        context["blog"] = self.get_parent().blogindexpage
        return context


class BlogListTagsIndexPage(ColdCMSPageMixin, Page):
    parent_page_types = []
    max_count_per_parent = 1
    show_in_menus_default = True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["tags_pages"] = BlogTagIndexPage.objects.all()
        return context


class BlogAuthorIndexPage(ColdCMSPageMixin, Page):
    author = models.ForeignKey(
        User, related_name="+", on_delete=models.SET_NULL, null=True
    )

    content_panels = Page.content_panels + [FieldPanel("author")]
    parent_page_types = []
    template = "blog/index_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["blog_pages"] = (
            BlogPage.objects.filter(owner=self.author)
            .live()
            .order_by("-first_published_at")
        )
        return context


class BlogListAuthorsIndexPage(ColdCMSPageMixin, Page):
    parent_page_types = []
    max_count_per_parent = 1
    show_in_menus_default = True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["authors_pages"] = BlogAuthorIndexPage.objects.all()
        return context


class BlogDateIndexPage(ColdCMSPageMixin, Page):
    date = models.DateField()

    content_panels = Page.content_panels + [FieldPanel("date")]
    parent_page_types = []
    template = "blog/index_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["blog_pages"] = BlogPage.objects.filter(
            date__year=self.date.year, date__month=self.date.month
        ).live()
        return context


class BlogListDatesIndexPage(ColdCMSPageMixin, Page):
    parent_page_types = []
    max_count_per_parent = 1
    show_in_menus_default = True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["dates_pages"] = BlogDateIndexPage.objects.all()
        return context
