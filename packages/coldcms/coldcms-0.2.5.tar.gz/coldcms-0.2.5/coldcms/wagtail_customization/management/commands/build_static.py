from coldcms.wagtail_customization.admin_views import build_static_pages
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        build_static_pages()
