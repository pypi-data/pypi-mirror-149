from coldcms.blog.models import (
    BlogListAuthorsIndexPage,
    BlogListDatesIndexPage,
    BlogListTagsIndexPage,
    BlogTagGroupByBlogPage,
)
from wagtail.core import hooks


@hooks.register("construct_explorer_page_queryset")
def dont_show_index_pages(parent_page, pages, request):
    return (
        pages.not_type(BlogListDatesIndexPage)
        .not_type(BlogListTagsIndexPage)
        .not_type(BlogListAuthorsIndexPage)
        .not_type(BlogTagGroupByBlogPage)
    )
