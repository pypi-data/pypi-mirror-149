from coldcms.wagtail_customization.image_formats import SrcsetFormat
from django import template
from django.utils.safestring import mark_safe
from wagtail.images.models import Image

register = template.Library()


def _generate_filters(ratio, method):
    return [f"{method}-{int(i*ratio)}x{i}" for i in [40, 80, 160, 360, 720]]


@register.simple_tag
def responsive_image(img: Image, classes="", ratio=4 / 3, method="fill"):
    filters = _generate_filters(ratio, method)
    srcset = SrcsetFormat("fullwidth", "Full width", classes, filters[0], filters)
    img_html = srcset.image_to_html(img, img.default_alt_text)
    return mark_safe(img_html)
