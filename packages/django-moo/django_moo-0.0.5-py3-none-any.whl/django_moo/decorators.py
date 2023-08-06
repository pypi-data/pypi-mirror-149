import inspect, types
from django.db.models.query import QuerySet
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django_moo.utils import QToDict, OrderSet
from functools import wraps

def controllor(func):
    @wraps(func)
    def deal(request, *args, **kwargs):
        context = func(request, *args, **kwargs)
        _package = inspect.getfile(func).split('\\')[-2]
        template_name = _package + '/' + func.__name__ + ".html"
        if isinstance(context, dict):
            return render(request, template_name, context)
        if isinstance(context, QuerySet):
            return render(request, template_name, {"ones":context})
        if isinstance(context, Model):
            return render(request, template_name, {"one": context})
        elif context is None:
            try:
                return render(request, template_name)
            except TemplateDoesNotExist:
                return render(request, 'django_moo/index.html')
        elif isinstance(context, HttpResponseBase):
            return context
        else:
            return HttpResponse(str(context))
    return deal

def rest_controllor(func):
    @wraps(func)
    def deal(request):
        queryset = func(request)
        if queryset is None:
            return JsonResponse([], safe=False)
        elif isinstance(queryset, dict):
            return JsonResponse(queryset)
        elif isinstance(queryset, Model) or isinstance(queryset, QuerySet):
            data = QToDict(queryset, request).get_result()
            if type(data) == list:
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse(data)
        elif isinstance(queryset, HttpResponseBase):
            return queryset
        else:
            return JsonResponse(queryset, safe=False)
    return deal

def url_pattern(url_path, isregex=False, **kwargs):  # url_path, isregex, name(template_name)
    def middle(func, context={}):
        @wraps(func)
        def inner(request, *args, **innerkwargs):
            result = func(request, *args, **innerkwargs)
            return result
        if not hasattr(url_pattern, "_all_func"):
            url_pattern._all_func = []
        context['url_path'] = url_path
        context['isregex'] = isregex
        context['func'] = func
        context['name'] = kwargs.get('name') or func.__name__
        url_pattern._all_func.append(context)
        return inner
    return middle

def redirect_to(to='/', permanent=False, ispath=True, **kwargs):  # direct_to(index)
    def middle(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                to = OrderSet(to) + 1
            except UnboundLocalError:
                to = '/'
            result = func(request, *args, **kwargs)
            if result is None:
                return redirect(to, permanent)
            if isinstance(result, HttpResponseBase):
                return result
            if isinstance(to, types.FunctionType):
                if isinstance(result, list) or isinstance(result, tuple):
                    return redirect(to, *result, permanent)
                elif isinstance(result, dict):
                    return redirect(to, permanent, **result)
                else:
                    return redirect(to, result, permanent)
            elif isinstance(to, str):
                if ispath:
                    if "{}" in to:
                        if isinstance(result, list) or isinstance(result, tuple):
                            return redirect(to.format(*result), permanent)
                        elif isinstance(result, dict):
                            return redirect(to.format(**result), permanent)
                        else:
                            return redirect(to.format(result), permanent)
                    else:
                        raise ValueError("you do not need to return any value.")
                else:
                    if isinstance(result, list) or isinstance(result, tuple):
                        return redirect(reverse(to, args=result), permanent)
                    elif isinstance(result, dict):
                        return redirect(reverse(to, kwargs=result), permanent)
                    else:
                        return redirect(reverse(to, args=[result,]), permanent)
            else:
                raise TypeError("'to' only require function or string")
        return inner
    if callable(to):
        return middle(to)  ## inner
    return middle