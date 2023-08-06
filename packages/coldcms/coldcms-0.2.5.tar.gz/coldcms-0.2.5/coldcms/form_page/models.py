from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtailyoast.edit_handlers import YoastPanel


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    post_form = RichTextField(blank=True)
    button = models.CharField(
        blank=True, default="", max_length=250, verbose_name=_("Button Text")
    )

    template = 'form_page/form_page.html'

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('button', classname="full"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('post_form', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=100, verbose_name=_("Key words"))
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(
                Page.promote_panels,
                heading=_("Promote")
            ),
            ObjectList(Page.settings_panels, heading=('Settings')),
            YoastPanel(
                keywords='keywords',
                title='seo_title',
                search_description='search_description',
                slug='slug'
            ),
        ]
    )

    def attached_form(self):
        return self.specific.get_form()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        previous_url = request.META.get('HTTP_REFERER')
        context['previous_url'] = previous_url
        return context

    class Meta:
        verbose_name = _("Form Page")
