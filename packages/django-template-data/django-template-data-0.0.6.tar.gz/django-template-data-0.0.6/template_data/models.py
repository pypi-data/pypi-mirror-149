from django.db import models
import json
from django.conf import settings


class TemplateData(models.Model):
    
    class TYPES:
        INTEGER = 'integer'
        FLOAT = 'float'
        STRING = 'string'
        MEDIA = 'media'
        JSON = 'json'        
        
    AVAILABLE_TYPES = [(TYPES.INTEGER, TYPES.INTEGER), (TYPES.FLOAT, TYPES.FLOAT),
                       (TYPES.STRING, TYPES.STRING), (TYPES.MEDIA, TYPES.MEDIA),
                       (TYPES.JSON, TYPES.JSON)]
    
    key = models.CharField(max_length=255)
    page = models.CharField(max_length=100, default='global')
    lang = models.CharField(max_length=100, choices=settings.LANGUAGES, null=True, blank=True)
    inherit_page = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=200, default='string', choices=AVAILABLE_TYPES)
    media = models.FileField(upload_to='data', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_value(self):
        if self.type == self.TYPES.STRING:
            return self.value
        elif self.type == self.TYPES.INTEGER:
            return int(self.value)
        elif self.type == self.TYPES.FLOAT:
            return float(self.value)
        elif self.type == self.TYPES.JSON:
            return json.loads(self.value)
        elif self.type == self.TYPES.MEDIA:
            return self.media

from .admin import *
