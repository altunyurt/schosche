# ~*~ coding:utf-8 ~*~

from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.utils import translation
from django.utils.translation import gettext, ngettext
from django.core.urlresolvers import reverse
from django.core.cache import cache
from jinja2 import FileSystemLoader, Environment
from urllib import quote
import jinja_filters as jf
import traceback
import os

__all__ =  ["jurl", "tuple_sorted_by_firstitem", "samelevel", "myenum", 
            "makeUrlDoc", "makeTaglist", "pagination", "plain_pagination", 
            "rgbshit", "quoted_colorlist"]

def jurl(view_name, *args, **kwargs):
    # reverse kısmında hakket args, kwargs diye parametre isimleri
    # varmış
    return reverse(view_name, args=args, kwargs=kwargs)

def tuple_sorted_by_firstitem(itemlist):
    def mycmp(a, b):
        return (a[0] > b[0] and 1) or (a[0]< b[0] and -1) or 0
    return sorted(itemlist, mycmp)

def samelevel(path, newdir):
    ''' mevcut seviyede başka bir dizine çeviriyor linki 
        /hede/hodo/loy -> /hede/hodo/ley
    '''
    return os.path.normpath(os.path.join(str(path), '..', str(newdir)))

def myenum(l):
    i = 1
    for item in l:
        yield (i, item)
        i += 1

def makeUrlDoc(cachedict):
    ''' çok özel fonskyion, bk gibi
        {u'_id': ObjectId('4c9538611d7c296b18000002'), u'value': 1.0}'dan Url dokumana çevir
    '''

    return Url(Urls.find_one({'_id':cachedict.get('_id')}))


def makeTaglist(length=15):
    taglist = cache.get(settings.CACHE_TAG_NAME)
    t = u""
    if not taglist:
        return t

    for tag in taglist[:length]:
        id = tag['_id']
        val = int(tag['value'])
        t += """<li><a href="/tags/%s/">%s<span class="right">%s</span></a></li>""" % (id, id, val)
    return t

def rewriteRequest(pagenum, request):
    req = '?page=%s' % pagenum
    if request:
        for key, val in request.GET.items():
            if key != 'page':
                req += '&%s=%s' % (key, val)
    return req

def ipag(number, i, req=None):
    ''' inner pagination '''
    if number == i:
        return "<li class='currentpage'><a href='%s'>%d</a></li>\n" % (rewriteRequest(i, req),i) 
    return "<li><a href='%s'>%d</a></li>\n" % (rewriteRequest(i, req),i) 

def pagination(page, req=None, step=10):
    total = page.paginator.num_pages

    if total == 1:
        return ""

    first = ipag(page.number, 1, req)
    last = ipag(page.number, total, req)

    tail = head = ""

    end = total - 1
    start = 2

    if page.number >= 2 + step:
        start = page.number - step
        head += '<li><span class="more" rel="%d-%d">...</span></li>\n' % (2, start)

    if page.number <= end - step:
        end = page.number + step
        tail += '<li><span class="more" rel="%d-%d">...</span></li>\n' % (end, total-1)

    data  = ''
    for i in range(start, end + 1):
         data += ipag(page.number, i, req)

    prev_link = u"<li class='previous disabled'>previous</li>\n" 
    if page.has_previous():
        prev_link = u"<li class='previous'><a href='%s'>« previous</a></li>\n" % rewriteRequest(page.previous_page_number(), req)

    next_link = u"<li class='next disabled'>next</li>\n" 
    if page.has_next():
        next_link = u"<li class='next'><a href='%s'>next »</a></li>\n" % rewriteRequest(page.next_page_number(), req)

    return u"<ul id='pagination' class='horizontal'>%s%s%s%s%s%s%s</ul>" %(prev_link, first, head, data, tail, last, next_link)


def plain_pagination(curr, total, req=None, step=10):

    if total == 1:
        return ""

    first = ipag(curr, 1, req)
    last = ipag(curr, total, req)

    tail = head = ""

    end = total - 1
    start = 2

    if curr > 2 + step:
        start = curr - step
        head += '<li><span class="page_more" rel="%d-%d">...</span></li>\n' % (2, start)

    if curr < end - step:
        end = curr + step
        tail += '<li><span class="page_more" rel="%d-%d">...</span></li>\n' % (end, total-1)

    data  = ''
    for i in range(start, end + 1):
         data += ipag(curr, i, req)

    prev_link = u"<li class='previous disabled'>previous</li>\n" 
    if curr > 1:
        prev_link = u"<li class='previous'><a href='%s'>« previous</a></li>\n" % rewriteRequest(curr - 1, req)

    next_link = u"<li class='next disabled'>next</li>\n" 
    if curr < total:
        next_link = u"<li class='next'><a href='%s'>next »</a></li>\n" % rewriteRequest(curr + 1, req)

    return u"<ul id='plain_pagination' class='horizontal'>%s%s%s%s%s%s%s</ul>" %(prev_link, first, head, data, tail, last, next_link)


def rgbshit(hexdata):
    return map(lambda x: int(str(x), 16), [hexdata[i:i+2]for i in range (1, len(hexdata), 2)])

def quoted_colorlist(palette):
    return ",".join([quote(color) for color in palette.get('colors')])
