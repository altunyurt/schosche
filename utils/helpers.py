# coding:utf-8

from django.conf import settings
from django.core.paginator import Paginator, Page
from random import choice
from string import lowercase, digits
import Crypto.Cipher.AES
import math 
import re
import sys


def generate_random_password(max_length=5):
    return "".join([choice(lowercase+digits) for i in range(max_length)])

def qsort(L):
    """quicksort"""
    if len(L) <= 1: return L
    return qsort( [ lt for lt in L[1:] if lt < L[0] ] )  +  \
                    [ L[0] ]  +  qsort( [ ge for ge in L[1:] if ge >= L[0] ] )


class myproperty(property):
    ''' 2.6+ style property decorator'''
    def __init__(self, fget, *args, **kwargs):
        self.__doc__ = fget.__doc__
        super(myproperty, self).__init__(fget, *args, **kwargs)

    def setter(self, fset):
        cls_ns = sys._getframe(1).f_locals
        for k, v in cls_ns.iteritems():
            if v == self:
                propname = k
                break
        cls_ns[propname] = myproperty(self.fget, fset,
                                    self.fdel, self.__doc__)
        return cls_ns[propname]



class SearchPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')
        super(SearchPaginator, self).__init__(*args, **kwargs)

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
            self._count = self.object_list.get_mset(0, self.db.get_doccount()).size()
        return self._count
    count = property(_get_count)

    """def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)"""


    def page(self, number, mobj):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        limit = bottom + self.per_page
        
        # self.object_list artık enquiry
        object_list = list(self.object_list.get_mset(bottom, limit))
        qs = list(mobj.find({'_id': 
                        {'$in': 
                         [ ObjectId(doc.document.get_value(settings.XAPIAN_MDB_OBJID)) for doc in object_list]}}))

        return Page(qs, number, self)

def paginate(objlist, numitems, pagenum):
    paginator = Paginator(objlist, numitems)
    return paginator.page(pagenum)

def spaginate(objlist, numitems, pagenum, db, mobj):
    paginator = SearchPaginator(objlist, numitems, db=db)
    return paginator.page(pagenum, mobj)

def sortascending(x,y):
    return x - y

def sortdescending(x,y):
    return y - x

def sort_dicts_by_key(dlist, k):
    def mycmp(a, b):
        return (a[k] > b[k] and 1) or (a[k]< b[k] and -1) or 0
    return sorted(dlist, mycmp)

def unicodeitems(d):
    temp = {}
    for key, val in d.items():
        if isinstance(val, basestring):
            val = val.strip()
            # convert string to unicode
            if isinstance(val, str):
                val = val.decode('utf-8')
        temp[key] = val
    return temp


def choices_to_dict(c):
    d = {}
    for key, val in c:
        d.update({key:val})
    return d
    


def tag_weight(x):
    if x==None or x==0:
         x = 1
    return math.log(x, math.e)



def pad16(s):
    return s.ljust(16)

def encrypt(salt, content):
    obj = Crypto.Cipher.AES.new(pad16(salt))
    return obj.encrypt(pad16(content))

def decrypt(salt, econtent):
    obj = Crypto.Cipher.AES.new(pad16(salt))
    return obj.decrypt(content)


def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.
    """
    # avoid a circular import
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}

    for fname in set(fields).difference(set(opts.get_all_field_names())):
        attr = getattr(instance, fname)
        data.update({fname:attr})


    for f in opts.fields + opts.many_to_many:
        if not f.editable:
            continue
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primry key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = [obj.pk for obj in f.value_from_object(instance)]
        else:
            data[f.name] = f.value_from_object(instance)
    return data


import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def html_unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
