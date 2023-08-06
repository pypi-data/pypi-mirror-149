from coldcms.blocks.blocks import ColoredBlock
from coldcms.blog.models import BlogIndexPage, BlogPage
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks


class BlogListValue(blocks.StructValue):
    @cached_property
    def blog_list(self):
        blog_list = BlogPage.objects.order_by("-date")[:self['number']]
        if self['page']:
            blog_list = self['page'].get_context(self)['blog_pages'][:self['number']]
        return blog_list


class BlogListBlock(ColoredBlock, blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, label=_("Title"))
    number = blocks.IntegerBlock(min_value=0, max_value=10, help_text=_("Number of article in the block."))
    page = blocks.PageChooserBlock(
        label=_("Link to an internal page"),
        help_text=_(
            "If none is selected, posts from all blogs will be displayed"
        ),
        required=False,
        page_type=BlogIndexPage,
    )

    class Meta:
        icon = "list-ul"
        label = _("List Blog Block")
        value_class = BlogListValue
