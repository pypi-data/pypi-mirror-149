from django.conf import settings as django_settings

DEFAULT_MOO_SETTINGS = {
    'APPS_ROUTE_PREFIX' : {},
    'DEFAULT_PER_PAGE' : 5
}

def get_setting():
    settings = DEFAULT_MOO_SETTINGS
    moo_settings = getattr(django_settings, 'DJANGO_MOO', {})
    for key in moo_settings:
        if key in settings:
            settings[key] = moo_settings[key]
    def validate_conf(conf_name, conf_type):
        if not isinstance(settings.get(conf_name), conf_type):
            raise TypeError("The {} type should be {}".format(conf_name, conf_type.__name__))
    validate_conf('APPS_ROUTE_PREFIX', dict)
    validate_conf('DEFAULT_PER_PAGE', int)
    return settings