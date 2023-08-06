from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
from template_data.models import TemplateData
from template_data.management.commands.add_data import DataMixin
import json


class Command(DataMixin, BaseCommand):
    """Install the theme"""

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="The json file where to store the data")

    def handle(self, *args, **options):
        file_name = options['file']

        try:
            data = {}

            for tpl_data in TemplateData.objects.all():
                data[tpl_data.key] = {'type': tpl_data.type, 'value': tpl_data.value, 'lang': tpl_data.lang,
                                      'page': tpl_data.page, 'inherit_page': tpl_data.inherit_page}

            with (settings.BASE_DIR / file_name).open('w') as fp:
                json.dump(data, fp)

            print(f"saved data to {file_name}")
        except Exception as e:
            import traceback

            traceback.print_exc()
