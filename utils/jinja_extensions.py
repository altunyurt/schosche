import jinja2
from jinja2.ext import Extension
import markdown2

class Markdown2Extension(Extension):
    tags = set(['markdown2'])

    def __init__(self, environment):
        super(Markdown2Extension, self).__init__(environment)
        environment.extend(
            markdowner=markdown2.Markdown()
        )   

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown2'],
            drop_needle=True
        )
        return jinja2.nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        return self.environment.markdowner.convert(caller()).strip()


'''
Created on 2009-12-30

@author: Jason Green
@author-email: guileen@gmail.com


in settings.py:
JINJA_EXTS=('jinja2.ext.i18n','youproject.app.extensions.csrf_token',)

use in jinja2 template just like django template:
<form ...>{% csrf_token %}...</form>
'''
from jinja2 import nodes
from jinja2.ext import Extension
from django.utils.safestring import mark_safe
import traceback


class CsrfExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        try:
            token = parser.stream.next()
            return nodes.Output([self.call_method('_render', [nodes.Name('csrf_token','load')])]).set_lineno(token.lineno)

        except:
            traceback.print_exc()

    def _render(self, csrf_token):
        """Helper callback."""
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return mark_safe(u"")
            else:
                return mark_safe(u"<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s' /></div>" % (csrf_token))
        else:
            # It's very probable that the token is missing because of
            # misconfiguration, so we raise a warning
            from django.conf import settings
            if settings.DEBUG:
                import warnings
                warnings.warn("A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")
            return u''

csrf_token=CsrfExtension
