import os

from coldcms.site_settings.models import VariablesColors
from django.conf import settings
from django.db.utils import OperationalError
from django.template import Context, Template
from django_assets import Bundle, register
from webassets.filter import Filter, register_filter

css_all_output = "css/app.css"
ORIGINAL_CSS_PATH = os.path.join(settings.STATIC_ROOT, f"{css_all_output}.original.css")


def _replace_original_css(_in, out, **kw):
    css_content = _in.read()
    out.write(css_content)
    os.makedirs(os.path.dirname(ORIGINAL_CSS_PATH), exist_ok=True)
    with open(ORIGINAL_CSS_PATH, "w") as f:
        f.write(css_content)


class AssetsSettings(Filter):
    name = "assets_settings"
    colors = {
        "black": settings.BLACK,
        "black_bis": settings.BLACK_BIS,
        "black_ter": settings.BLACK_TER,
        "grey_darker": settings.GREY_DARKER,
        "grey_dark": settings.GREY_DARK,
        "grey": settings.GREY,
        "grey_light": settings.GREY_LIGHT,
        "grey_lighter": settings.GREY_LIGHTER,
        "grey_lightest": settings.GREY_LIGHTEST,
        "white_ter": settings.WHITE_TER,
        "white_bis": settings.WHITE_BIS,
        "white": settings.WHITE,
        "orange": settings.ORANGE,
        "yellow": settings.YELLOW,
        "green": settings.GREEN,
        "turquoise": settings.TURQUOISE,
        "cyan": settings.CYAN,
        "blue": settings.BLUE,
        "purple": settings.PURPLE,
        "red": settings.RED,
        "primary": settings.PRIMARY,
        "info": settings.INFO,
        "success": settings.SUCCESS,
        "warning": settings.WARNING,
        "danger": settings.DANGER,
    }
    theme = settings.THEME_SCSS
    theme_variables = settings.THEME_VARIABLES_SCSS

    def get_colors(self):
        try:
            variables = VariablesColors.objects.first()
            if not variables:
                return self.colors
            for field in variables._meta.get_fields():
                if field.name in self.colors.keys():
                    self.colors[field.name] = getattr(variables, field.name)
        except OperationalError:
            return self.colors
        except VariablesColors.DoesNotExist:
            return self.colors
        return self.colors

    def input(self, _in, out, **kwargs):
        template = Template(_in.getvalue())
        context = Context({"colors": self.get_colors(), "theme": self.theme, "theme_variables": self.theme_variables})
        result = template.render(context)
        out.write(result)


register_filter(AssetsSettings)


scss = Bundle("scss/app.scss", filters="assets_settings,scss", output="css/app.scss")

css_all = Bundle(scss, filters="cssrewrite", output=css_all_output)

css_all = Bundle(css_all, filters=(_replace_original_css,), output=css_all_output)

register("css_all", css_all)
