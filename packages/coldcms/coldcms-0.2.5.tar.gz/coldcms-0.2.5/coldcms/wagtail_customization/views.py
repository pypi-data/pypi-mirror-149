from bakery.views import BuildableListView, BuildableTemplateView
from django.test.client import RequestFactory
from robots.views import RuleList
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core.models import Site


class SitemapTemplateView(BuildableTemplateView):
    build_path = 'sitemap.xml'
    template_path = 'sitemap.xml'

    def create_request(self, path):
        site = Site.objects.first()
        return RequestFactory(SERVER_NAME=site.hostname).get(path)

    def get(self, request, *args, **kwargs):
        self.context = self.get_context_data(**kwargs)
        return sitemap(request)


class RobotsListView(RuleList, BuildableListView):
    build_path = 'robots.txt'
    template_path = 'robots.txt'

    def create_request(self, path):
        site = Site.objects.first()
        return RequestFactory(SERVER_NAME=site.hostname).get(path)

    def get(self, request, *args, **kwargs):
        self.current_site = self.get_current_site(request)
        res = super().get(request, *args, **kwargs)
        return res
