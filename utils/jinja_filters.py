# ~*~ coding:utf-8 ~*~

from datetime import datetime
import re
from main.models import Day, Instructor, ClassRoom

__all__ = ["one", "timesince", 'myescape']

def one(data):
    if isinstance(data, list):
        return data[0] or ''
    return data

def timesince(timeval):

    delta = datetime.now() - timeval
    if delta.seconds < 60:
        return u"%d seconds" % int(delta.seconds)
    
    if delta.seconds < 3600:
        return u"%d minutes" % int(delta.seconds / 60)
    
    if delta.seconds < 3600*24:
        return  u"%d hour(s)" % int(delta.seconds/3600)
    
    return  u"%d days" % int(delta.seconds/3600)

def myescape(data):
    return re.sub('\r?\n', '<br>', data)

def colored_match(data, keyword, defidx=100):
    ''' kwnin indexini al'''
    if not keyword:
        return data 

    idx = data.find(keyword)
    start = 0
    end = len(data) - 1
    ''' id<100 ise komple baştan sonra al'''
    if idx > defidx:
        start = idx - defidx

    if idx < end - defidx:
        end = idx + defidx
    print idx, start, end

    result = data[start:end].replace(keyword, '<span class="matched">%s</span>' % keyword)
    return (start != 0 and u'...' or u'') + result + (end != len(data) -1 and u'...' or u'')

def getDay(data):
    return Day.objects.get(id=int(data))

def getInstructor(data):
    return Instructor.objects.get(id=int(data))

def getClassRoom(data):
    return ClassRoom.objects.get(id=int(data))


