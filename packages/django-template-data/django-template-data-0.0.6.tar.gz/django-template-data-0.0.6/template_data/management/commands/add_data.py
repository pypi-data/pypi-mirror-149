from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
from template_data.models import TemplateData
import json


class DataMixin:

    def add_data_in_json(self, key: str, d_type: str, value: str, lang: str, page: str,
                         inherit_page: str, file_name: str):
        data = {}
        try:
            with open(file_name) as fp:
                data = json.load(fp)
        except:
            pass

        data[key] = {'type': d_type, 'value': value, 'lang': lang, 'page': page, 'inherit_page': inherit_page}
        with open(file_name, 'w') as fp:
            json.dump(data, fp)

    def add_data_in_db(self, key: str, d_type: str, value: str, lang: str, page: str,
                       inherit_page: str):
        TemplateData.objects.update_or_create(key=key, page=page, lang=lang,
                                              defaults={'value': value, 'type': d_type, 'inherit_page': inherit_page})


class Command(DataMixin, BaseCommand):
    """Install the theme"""

    def add_arguments(self, parser):
        parser.add_argument("key", type=str, help="The key of the data")
        parser.add_argument("type", type=str, help="The type of the data")
        parser.add_argument("value", type=str, help="The value of the data")
        parser.add_argument("--lang", type=str, help="The lang of the data")
        parser.add_argument("--page", type=str, help="The page where the data apply", default='global')
        parser.add_argument("--file", type=str, help="The json file where to store the data")
        parser.add_argument("--inherit", type=str, help="Tells which page the data's page must inherit")

    def handle(self, *args, **options):
        print(f"options {options}")
        file_name = options['file']
        key = options['key']
        d_type = options['type']
        value = options['value']
        page = options['page']
        lang = options['lang']
        inherit_page = options['inherit']

        try:
            self.add_data_in_db(key, d_type, value, lang, page, inherit_page)

            if file_name:
                self.add_data_in_json(key, d_type, value, lang, page, inherit_page, file_name)
        except Exception as e:
            import traceback

            traceback.print_exc()
