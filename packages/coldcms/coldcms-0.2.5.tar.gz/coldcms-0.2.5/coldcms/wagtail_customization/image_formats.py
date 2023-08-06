from django.utils.html import escape
from PIL import Image
from wagtail.images.formats import (
    Format,
    get_rendition_or_not_found,
    register_image_format,
    unregister_image_format,
)
from wagtail.images.models import Image as WagtailImage


class SrcsetFormat(Format):
    def __init__(self, name, label, classnames, filter_spec, alt_filter_specs):
        super().__init__(name, label, classnames, filter_spec)
        self.alternative_filter_specs = alt_filter_specs

    def image_to_html(
        self, image: WagtailImage, alt_text: str, extra_attributes=""
    ):
        convert_to_jpg = ""
        with Image.open(image.file.path, "r") as pil_img:
            if pil_img.mode != "RGBA":
                convert_to_jpg = "|format-jpeg"

        rendition = get_rendition_or_not_found(
            image, self.filter_spec + convert_to_jpg
        )

        rendition_srcset = []
        for alt_filter_spec in self.alternative_filter_specs:
            rendition_srcset.append(
                get_rendition_or_not_found(
                    image, alt_filter_spec + convert_to_jpg
                )
            )

        if self.classnames:
            class_attr = f'class="{escape(self.classnames)}" '
        else:
            class_attr = ""

        srcsets = [f"{escape(r.url)} {r.width}w" for r in rendition_srcset]

        return (
            "<img "
            "{extra_attr}{classes}"
            'src="{src}" '
            'alt="{alt}" '
            'srcset="{srcset}">'.format(
                extra_attr=extra_attributes,
                classes=class_attr,
                src=escape(rendition.url),
                alt=escape(alt_text),
                srcset=", ".join(srcsets),
            )
        )


srcset = SrcsetFormat(
    "fullwidth",
    "Full width",
    "richtext-image full_width",
    "max-640x360",
    [
        "max-640x360",
        "max-768x432",
        "max-1024x576",
        "max-1600x900",
        "max-1920x1080",
    ],
)
unregister_image_format("fullwidth")
register_image_format(srcset)
