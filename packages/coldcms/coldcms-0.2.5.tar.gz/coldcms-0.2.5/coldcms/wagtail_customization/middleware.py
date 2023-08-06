from coldcms.form_page.models import FormPage
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware


class ColdCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Permission to post via a ColdCMS contact page without CSRF.
        The conditions are :
            - the path info is in the list of contact page urls.
            - the origin of the request is in the list of registered sites.
        """
        res = super().process_view(
            request, callback, callback_args, callback_kwargs
        )
        if request.method == "POST":
            # Get all registered sites
            valid_sites = settings.ALLOWED_HOSTS
            # Get all contact page urls exclude 'admin'
            valid_urls = [
                form_page.url for form_page in
                FormPage.objects.all() if "/admin/" not in form_page.url
            ]
            http_origin = request.META.get('HTTP_ORIGIN', False)
            if http_origin:
                http_origin = http_origin.split("//")[1]

            path_info = request.META.get('PATH_INFO', False)
            if (
                http_origin and http_origin in valid_sites
                and path_info and path_info in valid_urls
            ):
                return super()._accept(request)
        return res
