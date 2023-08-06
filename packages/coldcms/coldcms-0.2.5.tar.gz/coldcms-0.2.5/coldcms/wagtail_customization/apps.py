from coldcms.wagtail_customization.admin_views import (
    handle_delete,
    handle_publish,
    handle_save,
    handle_unpublish,
)
from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save
from wagtail.core.signals import page_published, page_unpublished


class WagtailCustomizationConfig(AppConfig):
    name = "coldcms.wagtail_customization"
    label = "wagtail_customization"

    def ready(self):

        page_published.connect(handle_publish)
        page_unpublished.connect(handle_unpublish)
        post_save.connect(handle_save)
        post_delete.connect(handle_delete)

    def disable_signals(self):
        """manually disable signals"""

        page_published.disconnect(handle_publish)
        page_unpublished.disconnect(handle_unpublish)
        post_save.disconnect(handle_save)
        post_delete.disconnect(handle_delete)
