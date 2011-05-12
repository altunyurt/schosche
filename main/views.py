# coding:utf-8 

from utils import render_to_response
from django.http import HttpResponse
from main.forms import *
from django.shortcuts import get_object_or_404

objects = {
    'course': Course,
    'lecturer': Lecturer,
    'coursetype': CourseType,
    'classroom': ClassRoom,
    'classroomtype': ClassRoomType
}

oforms = {
    'course': CourseForm,
    'lecturer': LecturerForm,
    'coursetype': CourseTypeForm,
    'classroom': ClassRoomForm,
    'classroomtype': ClassRoomTypeForm
}


def index(request):
    return render_to_response('index.jinja', locals())

def runconstraints(request):
    return HttpResponse('OK')


def addObject(request, objtype):
    _form = oforms.get(objtype)
    form = _form()
    if request.method == 'POST':
        form = _form(request.POST)
        if form.is_valid():
            obj = form.save()
            return HttpResponse(cjson.encode(obj.to_dict()))
    return HttpResponse('FAIL')
    

def editObject(request, objtype, objid):
    _obj = objects.get(objtype)
    _form = oforms.get(objtype)

    obj = get_object_or_404(_obj, id=objid)
    form = _form(instance=obj)
    if request.method == 'POST':
        form = _form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return HttpResponse(cjson.encode(obj.to_dict()))
    return HttpResponse('FAIL')


