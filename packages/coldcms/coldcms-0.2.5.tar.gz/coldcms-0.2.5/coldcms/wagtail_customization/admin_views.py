import contextlib
import logging
import os
import shutil
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from htmlmin.minify import html_minify
from wagtail.admin import messages
from wagtail.core import hooks

logger = logging.getLogger("static_generation")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# For now, we don't want to concurrently build a page
executor = ThreadPoolExecutor(max_workers=1)


ORIGINAL_CSS_SIZE = None


def _get_page_paths() -> [str]:
    return [str(path) for path in Path(settings.BUILD_DIR).glob("**/*.html")]


def get_custom_css():
    from coldcms.site_settings.models import CSSStyleSheet

    css_sheet = CSSStyleSheet.objects.first()

    if not css_sheet or not css_sheet.CSS_stylesheet:
        return None

    uploaded_file = css_sheet.CSS_stylesheet.file
    custom_css = uploaded_file.read()
    uploaded_file.close()
    return custom_css


def append_custom_css(app_css_path: str):
    custom_css = get_custom_css()
    if custom_css:
        with open(app_css_path, "ab") as outfile:
            outfile.write(custom_css)


def minify_css(page_paths: [str], app_css_path: str):

    from coldcms import assets

    global ORIGINAL_CSS_SIZE
    original_css_path = assets.ORIGINAL_CSS_PATH
    if os.path.exists(original_css_path):
        shutil.copyfile(original_css_path, app_css_path)

    append_custom_css(app_css_path)

    if not ORIGINAL_CSS_SIZE:
        ORIGINAL_CSS_SIZE = os.path.getsize(original_css_path)
    logger.debug(f"Start command - size of original css is {ORIGINAL_CSS_SIZE}")
    command = (
        ["purgecss", "--css", app_css_path, "--content"]
        + [",".join(page_paths)]
        + ["--output", os.path.dirname(app_css_path)]
    )
    try:
        out = subprocess.check_output(command)
        purge_app_css_size = os.path.getsize(app_css_path)
        logger.debug(f"End command={command}")
        logger.debug(f"Size of css after purge is {purge_app_css_size}")
        efficiency_purge = 100 - (purge_app_css_size * 100 / ORIGINAL_CSS_SIZE)
        logger.debug(f"Efficiency:  {efficiency_purge}%")
    except Exception:
        logger.exception(f"Error while trying to purge CSS, command={command}")
        logger.error("------------------------------------------------------------")
        logger.error("CSS cannot be minified")
        logger.error(
            "You should have purgecss installed and in you PATH to reduce the size of CSS files:"
        )
        logger.error("npm install -g purgecss@2.1.0 ")
        logger.error("More info: https://github.com/FullHuman/purgecss)")

        logger.error("------------------------------------------------------------")

    command = [
        "cleancss",
        "-O1",
        "specialComments:0",
        "--debug",
        "-o",
        app_css_path,
        app_css_path,
    ]
    try:
        out = subprocess.check_output(command)
        logger.debug(f"End command={command}, out={out}")
    except Exception:
        logger.exception(f"Error while trying to clean CSS, command={command}")
        logger.error("------------------------------------------------------------")
        logger.error("CSS cannot be minified")
        logger.error(
            "You should have cleancss installed and in you PATH to reduce the size of CSS files:"
        )
        logger.error("npm install -g clean-css-cli@4.3.0 ")
        logger.error("More info: https://www.npmjs.com/package/clean-css")
        logger.error("------------------------------------------------------------")


def minify_html(page_paths):
    for page_path in page_paths:
        with open(page_path, encoding="utf-8") as f:
            html = f.read()
            html_size = len(html)
            logger.debug(
                f"Start minify {page_path} - size of original html is {html_size}"
            )
        with open(page_path, "w", encoding="utf-8") as f:
            html_minified = html_minify(html)
            f.write(html_minified)
        html_minify_size = len(html_minified)
        logger.debug(f"Size of minify {page_path} is {html_minify_size}")
        if html_size > 0:
            efficiency_html = 100 - (html_minify_size * 100 / html_size)
            logger.debug(f"Efficiency: {efficiency_html}")


def minify_html_css(page_paths: [str], app_css_path: str):
    logger.debug("Start minifying CSS")
    minify_css(page_paths, app_css_path)
    logger.info("End minifying CSS")

    logger.debug("Start minifying HTML")
    minify_html(page_paths)
    logger.info("End minifying HTML")


def build_static_pages():
    from coldcms.assets import css_all
    from wagtailbakery.views import AllPublishedPagesView
    from django.urls import get_callable

    logger.debug("Start building flat files")
    view = AllPublishedPagesView()
    if view.get_queryset():
        view.build_method()
        sitemap_view = get_callable('coldcms.wagtail_customization.views.SitemapTemplateView')
        sitemap_view().build_method()
        robots_view = get_callable('coldcms.wagtail_customization.views.RobotsListView')
        robots_view().build_method()
    logger.debug("End building flat files")
    app_css_path = os.path.join(settings.STATIC_ROOT, css_all.output)
    page_paths = _get_page_paths()
    minify_html_css(page_paths, app_css_path)


def build_static_pages_async():
    # don't hide the slowness in development
    if settings.DEBUG:
        build_static_pages()
    else:
        executor.submit(build_static_pages)


def delete_cached_files():
    logger.debug("Start deleting existing cached files")
    page_paths = _get_page_paths()
    for page_path in page_paths:
        with contextlib.suppress(FileNotFoundError):
            os.remove(page_path)
    logger.debug("End deleting existing cached files")


def handle_publish(sender=None, instance=None, revision=None, **kwargs):
    build_static_pages_async()


def handle_unpublish(sender=None, instance=None, revision=None, **kwargs):
    delete_cached_files()
    build_static_pages_async()


def handle_save(
    sender=None,
    instance=None,
    created=None,
    raw=None,
    using=None,
    update_fields=None,
    revision=None,
    **kwargs,
):
    from wagtail.images.models import Image
    from coldcms.assets import css_all
    from coldcms.site_settings.models import (
        SiteSettings,
        FooterColumn,
        CSSStyleSheet,
        VariablesColors,
        MenuOptions,
    )
    from wagtail.documents.models import Document
    from wagtail.core.models import Site

    if (
        sender == Document
        and CSSStyleSheet.objects.filter(CSS_stylesheet=instance).exists()
    ):
        handle_publish(sender, instance, revision, **kwargs)

    # don't re-build if Image was just created (and isn't used anywhere yet)
    # re-build if Logo, Footer or Sites was modified in Settings
    if (sender == Image and created is False) or sender in {
        SiteSettings,
        FooterColumn,
        Site,
        CSSStyleSheet,
        VariablesColors,
        MenuOptions,
    }:
        if sender == VariablesColors:
            css_all.build(force=True, disable_cache=True)
        handle_publish(sender, instance, revision, **kwargs)


def handle_delete(sender=None, instance=None, revision=None, **kwargs):
    from wagtail.images.models import Image
    from coldcms.site_settings.models import FooterColumn
    from wagtail.documents.models import Document
    from wagtail.core.models import Site

    if sender in {
        FooterColumn,
        Site,
        Image,
        Document,
    }:
        handle_publish(sender, instance, revision, **kwargs)


# TODO replace by https://github.com/wagtail/wagtail/pull/5169 when released
# (can also be used to know when a page is moved relatively to its siblings)
@hooks.register("after_move_page")
def handle_after_move_page(request, page):
    build_static_pages_async()


@csrf_protect
@staff_member_required
@require_http_methods(["GET", "POST"])
def generate_statics(request, page_id):
    from wagtail.core.models import Page

    page = get_object_or_404(Page, id=page_id).specific

    if request.method == "GET":
        return render(
            request,
            "wagtail_customization/confirm_generate_statics.html",
            {"page": page},
        )

    try:
        delete_cached_files()
        build_static_pages_async()
        messages.success(request, _("Page successfully generated"))
    except Exception:
        logger.exception("Couldn't generate statics")
        messages.error(request, _("Couldn't re-generate page"))

    return redirect("wagtailadmin_explore", page.pk)
