import pytest
from coldcms.generic_page.models import GenericPage
from coldcms.site_settings.models import Footer, FooterColumn, SiteSettings
from coldcms.site_settings.templatetags.site_tags import get_footer_columns
from coldcms.wagtail_customization import admin_views
from django.db.models.signals import post_save
from factory.django import mute_signals
from wagtail.core.models import Site

pytestmark = pytest.mark.django_db
send_count = 0


def patched_handle_publish(*args, **kwargs):
    global send_count
    send_count += 1


def test_get_footer_columns():
    home = GenericPage.objects.create(title="My Home", path="/path/", depth=666)
    site = Site.objects.create(root_page=home)
    footer = Footer.objects.create(site=site)
    with mute_signals(post_save):
        FooterColumn.objects.create(footer=footer, title="Helo")
    columns = list(get_footer_columns())
    assert columns[0].title == "Helo"


def test_get_footer_columns_empty():
    assert get_footer_columns() == []


def test_footer():
    footer = Footer()
    assert str(footer) == "Footer"


@pytest.mark.enable_signals
def test_footer_column_saved_calls_statics_build(monkeypatch):
    monkeypatch.setattr(admin_views, "handle_publish", patched_handle_publish)

    home = GenericPage.objects.create(title="My Home", path="/path/", depth=666)
    with mute_signals(post_save):
        site = Site.objects.create(root_page=home)
    footer = Footer.objects.create(site=site)
    column = FooterColumn(footer=footer)

    global send_count
    assert send_count == 0
    column.save()
    assert send_count == 1
    send_count = 0


@pytest.mark.enable_signals
def test_footer_column_deleted_calls_statics_build(monkeypatch):
    monkeypatch.setattr(admin_views, "handle_publish", patched_handle_publish)

    home = GenericPage.objects.create(title="My Home", path="/path/", depth=666)

    with mute_signals(post_save):
        site = Site.objects.create(root_page=home)
        footer = Footer.objects.create(site=site)
        column = FooterColumn.objects.create(footer=footer)

    global send_count
    assert send_count == 0
    column.delete()
    assert send_count == 1
    send_count = 0


@pytest.mark.enable_signals
def test_site_settings_saved_calls_statics_build(monkeypatch):
    monkeypatch.setattr(admin_views, "handle_publish", patched_handle_publish)

    home = GenericPage.objects.create(title="My Home", path="/path/", depth=666)

    with mute_signals(post_save):
        site = Site.objects.create(root_page=home)

    site_settings = SiteSettings(site=site)

    global send_count
    assert send_count == 0
    site_settings.save()
    assert send_count == 1
    send_count = 0
