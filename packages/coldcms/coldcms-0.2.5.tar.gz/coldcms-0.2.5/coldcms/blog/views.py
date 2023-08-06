from coldcms.blog.models import (
    BlogAuthorIndexPage,
    BlogDateIndexPage,
    BlogIndexPage,
    BlogListAuthorsIndexPage,
    BlogListDatesIndexPage,
    BlogListTagsIndexPage,
    BlogPage,
    BlogTagGroupByBlogPage,
    BlogTagIndexPage,
)
from coldcms.wagtail_customization.admin_views import handle_publish
from coldcms.wagtail_customization.apps import WagtailCustomizationConfig
from django.apps import apps
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


def get_tags_to_clean(exclude=None):
    pages = BlogPage.objects.all().live().prefetch_related("tags")
    used_tags = set(
        tag for blog_page in pages
        for tag in blog_page.tags.all()
    )
    existing_tag_index_pages = {
        blog_tag_index.tag for blog_tag_index
        in BlogTagIndexPage.objects.all().select_related("tag")
    }
    return used_tags, existing_tag_index_pages


def get_tags_by_blog_to_clean(blog):
    pages = BlogPage.objects.child_of(blog).live().prefetch_related("tags")
    used_blog_tags = set(
        tag for blog_page in pages
        for tag in blog_page.tags.all()
    )
    existing_blog_tag_pages = {
        blog_tag_index.tag for blog_tag_index
        in BlogTagGroupByBlogPage.objects.child_of(blog).select_related("tag")
    }
    return used_blog_tags, existing_blog_tag_pages


def get_authors_to_clean():
    pages = BlogPage.objects.all().live().prefetch_related("tags")
    existing_users = {blog_page.owner for blog_page in pages}
    existing_author_index_pages = {
        blog_author_index.author
        for blog_author_index in BlogAuthorIndexPage.objects.all()
    }
    return existing_users, existing_author_index_pages


def get_dates_to_clean():
    pages = BlogPage.objects.all().live().prefetch_related("tags")
    existing_dates = {
        blog_page.date.replace(day=1) for blog_page in pages
    }
    existing_date_index_pages = {
        blog_date_index.date.replace(day=1)
        for blog_date_index in BlogDateIndexPage.objects.all()
    }
    return existing_dates, existing_date_index_pages


def refresh_tags_groupby_blog(instance):
    blog = instance.get_parent()
    used_blog_tags, existing_blog_tag_pages = get_tags_by_blog_to_clean(blog)
    tags_to_remove = existing_blog_tag_pages - used_blog_tags
    tags_to_add = used_blog_tags - existing_blog_tag_pages
    BlogTagGroupByBlogPage.objects.child_of(blog).filter(
        tag__in=tags_to_remove
    ).delete()
    for tag in tags_to_add:
        new_tag_groupby_blog_page = BlogTagGroupByBlogPage(
            title=_(f"Tag {tag.name} group by blog {blog.title}"),
            tag=tag,
            slug=slugify(tag.name),
        )
        blog.add_child(instance=new_tag_groupby_blog_page)
        new_tag_groupby_blog_page.save_revision().publish()


def refresh_tags():
    used_tags, existing_tag_index_pages = get_tags_to_clean()
    tags_to_remove = existing_tag_index_pages - used_tags
    tags_to_add = used_tags - existing_tag_index_pages

    BlogTagIndexPage.objects.filter(tag__in=tags_to_remove).delete()

    parent_page = BlogListTagsIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListTagsIndexPage(
            title=_("Tags"), slug="tags", show_in_menus=False
        )
        home = BlogIndexPage.get_first_root_node().get_first_child().genericpage
        home.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for tag in tags_to_add:
        new_tag_page = BlogTagIndexPage(
            title=_(f"Blog posts tagged {tag.name}"),
            tag=tag,
            slug=slugify(tag.name),
        )
        parent_page.add_child(instance=new_tag_page)
        new_tag_page.save_revision().publish()


def refresh_authors():
    existing_users, existing_author_index_pages = get_authors_to_clean()
    authors_to_remove = existing_author_index_pages - existing_users
    authors_to_add = existing_users - existing_author_index_pages

    BlogAuthorIndexPage.objects.filter(author__in=authors_to_remove).delete()

    parent_page = BlogListAuthorsIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListAuthorsIndexPage(
            title=_("Authors"), slug="authors", show_in_menus=False
        )
        home = BlogIndexPage.get_first_root_node().get_first_child().genericpage
        home.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for author in authors_to_add:
        new_index_page = BlogAuthorIndexPage(
            title=_("Blog posts by %(author)s") % {"author": author.username.title()},
            author=author,
            slug=slugify(author.username),
        )
        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()


def refresh_dates():
    existing_dates, existing_date_index_pages = get_dates_to_clean()
    dates_to_remove = existing_date_index_pages - existing_dates
    dates_to_add = existing_dates - existing_date_index_pages

    BlogDateIndexPage.objects.filter(date__in=dates_to_remove).delete()

    parent_page = BlogListDatesIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListDatesIndexPage(
            title=_("Dates"), slug="dates", show_in_menus=False
        )
        home = BlogIndexPage.get_first_root_node().get_first_child().genericpage
        home.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for date in dates_to_add:
        new_index_page = BlogDateIndexPage(
            title=_("Blog posts published on %(date)s")
            % {"date": date.strftime("%B, %Y")},
            date=date,
            slug=slugify(date.strftime("%B-%Y")),
        )

        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()


def refresh_index_pages(sender=None, instance=None, revision=None, **kwargs):
    # Disabled signals to build page
    app_config = apps.get_app_config(WagtailCustomizationConfig.label)
    app_config.disable_signals()

    refresh_tags_groupby_blog(instance)
    refresh_tags()
    refresh_authors()
    refresh_dates()
    # Publish one time at the end of refresh blog pages.
    handle_publish()
    # Enabled signals to build pages
    app_config.ready()


def unpublish_before_delete(sender=None, instance=None, revision=None, **kwargs):
    instance.unpublish()
