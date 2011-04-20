from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url('^$', 'index', name='index'),
)
