import os

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('theme_name', type=str)
        parser.add_argument(
            '--directory',
            help='Directory where theme will be created, root of coldcms by default',
            type=str
        )

    def handle(self, *args, **options):
        theme = options['theme_name']

        if options['directory']:
            if os.path.exists(options['directory']):
                theme_dir = options['directory']
            else:
                self.stderr.write('Error, directory ' + options['directory'] + ' don\'t exist')
                return
        else:
            theme_dir = settings.BASE_DIR
        try:
            os.mkdir(os.path.join(theme_dir, theme))
            os.mkdir(os.path.join(theme_dir, theme, 'static'))
            os.mkdir(os.path.join(theme_dir, theme, 'static', 'scss'))
            with open(os.path.join(theme_dir, theme, "static", "scss", f"_{theme}.scss"), 'a') as scss_file:
                scss_file.write(f"/* --------- Your theme {theme} ---------- */")
            with open(os.path.join(theme_dir, theme, "static", "scss", f"_{theme}_variables.scss"), 'a') as scss_file:
                scss_file.write(f"/* --------- Your theme variables {theme} ---------- */")
            os.mkdir(os.path.join(theme_dir, theme, 'static', 'svg'))
            os.mkdir(os.path.join(theme_dir, theme, 'templates'))
        except FileExistsError:
            self.stderr.write('Error : This theme already has files and directories')
            return
