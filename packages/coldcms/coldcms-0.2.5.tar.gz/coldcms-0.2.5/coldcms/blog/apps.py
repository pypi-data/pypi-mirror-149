from django.apps import AppConfig
from django.db.models.signals import pre_delete
from wagtail.core.signals import page_published, page_unpublished


class BlogConfig(AppConfig):
    name = "coldcms.blog"

    def ready(self):
        from coldcms.blog.models import BlogPage
        from coldcms.blog.views import (
            refresh_index_pages, unpublish_before_delete
        )
        page_published.connect(refresh_index_pages, sender=BlogPage)
        page_unpublished.connect(refresh_index_pages, sender=BlogPage)
        pre_delete.connect(unpublish_before_delete, sender=BlogPage)
