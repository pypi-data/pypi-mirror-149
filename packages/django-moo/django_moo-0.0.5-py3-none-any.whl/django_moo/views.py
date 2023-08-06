from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django_moo.decorators import rest_controllor
from django.shortcuts import redirect, render
# def quick_view(value):
#     return controllor(lambda request: value)

def quick_view(str_name, **context):
    def view(request):
        if isinstance(str_name, str):
            if str_name.endswith('.html'):
                try:
                    return render(request, str_name, context)
                except TemplateDoesNotExist:
                    return HttpResponse(str_name)
            return HttpResponse(str_name)
        return HttpResponse(str(str_name))
    return view

def rest_quick_view(rest):
    return rest_controllor(lambda request: rest)


def quick_redirect(path, *args, permanent=True, **kwargs):
    return lambda request: redirect(path, *args, permanent, **kwargs)