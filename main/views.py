# coding:utf-8 

from utils import render_to_response
from django.http import HttpResponse
from main.forms import *
from django.shortcuts import get_object_or_404

objects = {
    'course': Course,
    'instructorr': Instructor,
    'classroom': ClassRoom,
    'classroomtype': ClassRoomType
}

oforms = {
    'course': CourseForm,
    'instructor': InstructorForm,
    'classroom': ClassRoomForm,
    'classroomtype': ClassRoomTypeForm
}


def index(request):
    ''' burası tüm listenin görüneceği yer '''
    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        sch = None
    return render_to_response('index.jinja', locals())

def show_term(request):
    term = request.GET('term', 1)
    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        sch = None

    return render_to_response('show_term.jinja', locals())

def runconstraints(request):
    return HttpResponse('OK')


def addObject(request, objtype):
    _form = oforms.get(objtype)
    form = _form()
    if request.method == 'POST':
        form = _form(request.POST)
        if form.is_valid():
            obj = form.save()
            #return HttpResponse(cjson.encode(obj.to_dict()))
    #return HttpResponse('FAIL')
    return render_to_response('form.jinja', locals())
    

def editObject(request, objtype, objid):
    _obj = objects.get(objtype)
    _form = oforms.get(objtype)

    obj = get_object_or_404(_obj, id=objid)
    form = _form(instance=obj)
    if request.method == 'POST':
        form = _form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            #return HttpResponse(cjson.encode(obj.to_dict()))
    #return HttpResponse('FAIL')
    return render_to_response('form.jinja', locals())


