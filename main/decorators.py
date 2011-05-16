# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from utils import render_to_response
from datetime import datetime, timedelta
max_age = 2592000 # 30 gün


__all__  =  [ 'requires_anonymous', 'requires_post','requires_login', 'under_construction']

def requires_post(f):
    def inner(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponse('POST required')
        return f(request, *args, **kwargs)
    return inner

def requires_anonymous(f):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return f(request, *args, **kwargs)
    return inner

def requires_login(f):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            response = HttpResponseRedirect('/login/')
            response.set_cookie('next', request.path)
            return response
        return f(request, *args, **kwargs)
    return inner

def under_construction(f):
    def inner(request, *args, **kwargs):
        return render_to_response('duz/under_construction.jinja', locals())
    return inner


