import json
import os

from coldcms.generic_page.models import GenericPage
from coldcms.wagtail_customization.apps import WagtailCustomizationConfig
from django.apps import apps
from django.core.files.images import ImageFile
from django.core.management import BaseCommand
from wagtail.core.models import Page, Site
from wagtail.images.models import Image


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--noconfirm", action="store_true", help="don't ask for confirmation",
        )

    def handle(self, *args, **options):
        if not options["noconfirm"]:
            result = input(
                "You should only run this command once. Are you sure "
                "you want to continue? (y/N)"
            )
            if result.lower() != "y":
                print("No action taken. Exiting.")
                return

        app_config = apps.get_app_config(WagtailCustomizationConfig.label)
        app_config.disable_signals()

        try:
            print("Creating initial data...")
            self._create_data()
            print("Initial data created")
        except Exception as e:
            print("Error:", e)
        finally:
            app_config.ready()

    def _create_data(self):
        site = Site.objects.first()
        homepage = Page.objects.filter(path="00010001")
        if homepage and isinstance(homepage.first().specific, GenericPage):
            print("Welcome page already set up")
            return
        # delete default welcome page
        homepage.delete()
        # create our own default page
        home = GenericPage.objects.create(title="ColdCMS", path="00010001", depth=2)
        site.root_page = home
        site.save()
        root = site.root_page.get_root()
        root.numchild = 1
        root.save()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        carousel_image = Image.objects.create(
            title="forest.jpg",
            file=ImageFile(
                open(os.path.join(current_dir, "images", "forest.jpg"), "rb")
            ),
            width=5184,
            height=3456,
        )
        lang = os.getenv("LANG", "en")
        if "fr_fr" in lang.lower():
            home.content_blocks = json.dumps(
                [
                    {
                        "type": "carousel",
                        "value": {
                            "title": None,
                            "slides": [
                                {
                                    "title": "Bienvenue sur votre instance ColdCMS",
                                    "text": "Explorez l'interface admin pour ajouter des pages !",
                                    "buttons": [
                                        {"text": "Administrer", "extra_url": "/admin/"}
                                    ],
                                    "image": {
                                        "image_type": 'image',
                                        "img": carousel_image.pk,
                                    },
                                }
                            ],
                        }
                    }
                ]
            )
        else:
            home.content_blocks = json.dumps(
                [
                    {
                        "type": "carousel",
                        "value": {
                            "title": None,
                            "slides": [
                                {
                                    "title": "Welcome to your ColdCMS instance",
                                    "text": "Explore admin interface to add new pages!",
                                    "buttons": [
                                        {"text": "Administrate", "extra_url": "/admin/",}
                                    ],
                                    "image": {
                                        "image_type": 'image',
                                        "img": carousel_image.pk,
                                    },
                                }
                            ],
                        }
                    }
                ]
            )

        home.save_revision().publish()
