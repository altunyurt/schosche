# coding:utf-8 

from utils import render_to_response
from django.http import HttpResponse
from main.forms import *
from django.shortcuts import get_object_or_404
from utils.constraints import *
from django.contrib.auth import login as _login, logout as _logout, authenticate
from main.decorators import * 

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

    vtype = request.GET.get('view', 'course')

    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        sch = None
    return render_to_response('index.jinja', locals())

def runconstraints(request):
    domains = {}
    constraints = []

    ''' her ders için zaten veri girişind uygulanan kısıtlara göre domain oluştur'''
    courses = Course.objects.filter(is_active=True)
    for course in courses:
        values = [(int(instructor.id), int(room.id), int(day.id), hour)
                    for instructor in course.instructors.filter(is_active=True)
                        for room in course.rooms.filter(is_active=True)
                            for day in course.days.all()
                                for hour in range(9, 19-course.duration)]
        domains[course] = fd.FiniteDomain(values)

    for course1 in courses:
        for course2 in courses:
            if course1 != course2:
                c = SameDaySameRoomConstraint((course1, course2))
                constraints.append(c)

    r = Repository(courses, domains, constraints)
    s = Solver()
    s.distrib_cnt = 0
    s.max_depth = 0
    s.verbose = 0
    x = s._solve(r)
    print x.next()

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


def login(request):
    return render_to_response('login.jinja', locals())

def logout(request):
    # çıkışta direk anasayfaya atıyoruz
    return render_to_response('login.jinja', locals())
