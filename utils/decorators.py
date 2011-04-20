# ~*~ coding:utf-8 ~*~

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class AnonymousRequired( object ):
    def __init__( self, redirect_to='/home/'):
        self.redirect_to = redirect_to
 
    def __call__( self, view_func):
        def wrapped_func(request, *args, **kwargs):
            if request.user is not None and request.user.is_authenticated():
                return HttpResponseRedirect( self.redirect_to ) 
            return view_func( request, *args, **kwargs)
        return wrapped_func

def needUsername(f):
    def inner(request, *args, **kwargs):
        if request.user.username in (u'', None):
            return HttpResponseRedirect(reverse('show_account'))
        return f(request, *args, **kwargs)
    return inner

def shouldBeNameless(f):
    def inner(request, *args, **kwargs):
        if request.user.username not in (u'', None):
            return HttpResponseRedirect(reverse('home'))
        return f(request, *args, **kwargs)
    return inner

def adminRequired(f):
    def inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('admin_login'))
        return f(request, *args, **kwargs)
    return inner

