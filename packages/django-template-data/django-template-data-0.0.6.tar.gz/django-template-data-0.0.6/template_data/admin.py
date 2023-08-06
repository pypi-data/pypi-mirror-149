from django.contrib import admin
from template_data.models import TemplateData
from django.conf import settings
from django.urls import URLPattern, URLResolver, NoReverseMatch
from django import forms
from django.urls import get_resolver

try:
    URL_EX_PREFIXES = settings.URL_CHOICES_EXLUDE_PREFIXES
except:
    URL_EX_PREFIXES = ['admin/']


def get_url_choices():    
    try:
        urlpatterns = get_resolver().url_patterns
    except NoReverseMatch:
        pass
    
    def list_urls(lis, acc=None):
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        
        if isinstance(l, URLPattern):
            url_name = l.name
            if url_name:
                yield url_name #+ f" ({str(l.pattern)})"
            #else:
            #    yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            desc_pattern = l.pattern.describe()
            desc_pattern = desc_pattern.replace("'", "")
                
            if desc_pattern not in URL_EX_PREFIXES:
                yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
        
        yield from list_urls(lis[1:], acc)
    
    res = [('global','global')]
    for url in list_urls(urlpatterns):
        pair = (''.join(url), ''.join(url))
        if pair not in res:
            res.append(pair)
    return res


    
class TemplateDataForm(forms.ModelForm):
    page = forms.ChoiceField(choices=get_url_choices)

@admin.register(TemplateData)
class TemplateDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', 'lang', 'key', 'value', 'type']
    form = TemplateDataForm
