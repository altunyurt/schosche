# ~*~ coding:utf-8 ~*~

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.utils import translation
from django.utils.translation import gettext, ngettext
from django.core.urlresolvers import reverse
from jinja2 import FileSystemLoader, Environment
from jinja_methods import * 
from urlparse import urlparse
import jinja_filters as jf
import traceback


class DjangoTranslator(object):

    def __init__(self):
        self.gettext = gettext
        self.ngettext = ngettext

class DjangoEnvironment(Environment):

    def get_translator(self, context):
        return DjangoTranslator()


template_dirs = getattr(settings,'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
global_exts = getattr(settings, 'JINJA_EXTENSIONS', [])
global_exts.append('utils.jinja_extensions.CsrfExtension')

env = DjangoEnvironment(autoescape=False, loader=FileSystemLoader(template_dirs, encoding="utf-8"), extensions=global_exts)
env.filters.update({'myescape':jf.myescape,
                    'colored_match':jf.colored_match})
env.install_gettext_translations(translation)

additional_context = {'settings':settings, 
                      'getattr':getattr, 
                      'enumerate': myenum,
                      'url_for': jurl,
                      'str': str,
                      'int': int,
                      'pagination': pagination
                     }

def render_to_string(filename, context={}, context_instance=Context({}), mimetype=default_mimetype):
    _context = {}
    
    template = env.get_template(filename)
    request = context.get('request')

    for d in context_instance.dicts:
        _context.update(d)
    for d in RequestContext(request, context):
        _context.update(d)
    _context.update({'user':request.user})
    _context.update(additional_context)
    return template.render(**_context)

def render_to_mail_string(filename, context={}, context_instance=Context({}), mimetype=default_mimetype):
    template = env.get_template(filename)
    context.update(additional_context)
    return template.render(**context)
    

# jinja için gerekli bu kısım
def render_to_response(filename, context={}, context_instance=Context({}), mimetype=default_mimetype):
    rendered = render_to_string(filename, context=context, context_instance=context_instance,
                                mimetype=mimetype)
    return HttpResponse(rendered, mimetype=mimetype)


