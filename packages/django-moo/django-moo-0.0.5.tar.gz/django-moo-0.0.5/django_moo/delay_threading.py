from django_moo.decorators import url_pattern 
from django.urls import path, re_path, get_resolver
from django_moo.utils import get_objs_all_attr
from django_moo.moost import get_setting
from django.conf import settings as django_settings
from django_moo import DIR_PATH

def delay_conduct():
    print('[django_moo] url_pattern is working on ...')
    set_path()
    set_static()

def set_path():
    apps_route_prefix = get_setting().get('APPS_ROUTE_PREFIX')
    if not hasattr(url_pattern, '_all_func'):
        url_pattern._all_func = []
    url_patterns = get_resolver().url_patterns
    for c in url_pattern._all_func:
        url_path = c.get('url_path')
        func = c.get('func')
        name = c.get('name')
        app_name = func.__module__.split('.')[0]   
        prefix = apps_route_prefix.get(app_name)
        if prefix is None:
            prefix = app_name + '/'
        url_path = prefix + url_path
        if c.get('isregex'):
            p = re_path(url_path, func, name=name)
        else:
            p = path(url_path, func, name=name)
        if p.name not in get_objs_all_attr(url_patterns, name):
            url_patterns.append(p)

def set_static():
    dir = DIR_PATH + 'static'
    django_settings.STATICFILES_DIRS.append(dir)