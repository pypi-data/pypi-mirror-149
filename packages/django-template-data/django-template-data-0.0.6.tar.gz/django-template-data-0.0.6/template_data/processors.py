from template_data.models import *
from django.urls import resolve
from django.db.models import Q
import re
from django.conf import settings
from django.utils.translation import get_language
try:
    from meta.views import Meta
    HAS_META = True
except:
    HAS_META = False
    
    
def load_meta(request):
    url_name = resolve(request.path_info).url_name
    if not url_name:
        url_name = request.path
    lang = get_language()
                
    tpl_datas = list(TemplateData.objects.filter(Q(page='global')|\
                        (Q(page=url_name)), key__startswith="meta_").filter(Q(lang=lang)|Q(lang__isnull=True)))
    needed_pages = [tpl_data.inherit_page for tpl_data in tpl_datas \
                    if tpl_data.inherit_page != None]
    needed_datas = {(tpl_data.key, tpl_data.page):tpl_data.get_value() for \
                tpl_data in TemplateData.objects.filter(page__in=needed_pages)}
    
    metas = {}
    for tpl_data in tpl_datas:
        if tpl_data.key.startswith('meta_'):
            meta_key = tpl_data.key.replace('meta_', '').lower()
            
            if not tpl_data.inherit_page:
                metas[meta_key] = tpl_data.get_value()
            else:
                tmp_value = tpl_data.get_value()
                metas[meta_key] = re.sub("{{ *super *}}", 
                                needed_datas[(tpl_data.key, tpl_data.inherit_page)],
                                tmp_value)
        
    return {'meta':Meta(**metas)}


def load_data(request):
    url_name = resolve(request.path_info).url_name
    if not url_name:
        url_name = request.path

    lang = get_language()
        
    tpl_datas = list(TemplateData.objects.filter(Q(page='global')|\
                        (Q(page=url_name))).filter(Q(lang=lang)|Q(lang__isnull=True)))
    needed_pages = [tpl_data.inherit_page for tpl_data in tpl_datas \
                    if tpl_data.inherit_page != None]
    needed_datas = {(tpl_data.key, tpl_data.page):tpl_data.get_value() for \
                tpl_data in TemplateData.objects.filter(page__in=needed_pages)}
    
    res = {}
    for tpl_data in tpl_datas:
        if not tpl_data.inherit_page:
            res[tpl_data.key] = tpl_data.get_value()
        else:
            tmp_value = tpl_data.get_value()
            try:
                res[tpl_data.key] = re.sub("{{ *super *}}", 
                                needed_datas[(tpl_data.key, tpl_data.inherit_page)],
                                tmp_value)
            except:
                res[tpl_data.key] = tmp_value
                
    if HAS_META and getattr(settings, 'TEMPLATE_DATA_LOAD_META', True):
        res.update(load_meta(request))
    
    return res   
