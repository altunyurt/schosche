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
    sch = None
    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        pass 

    return render_to_response('index.jinja', locals())

def runconstraints(request):
    domains = {}
    constraints = []

    ''' her ders için zaten veri girişind uygulanan kısıtlara göre domain oluştur'''
    courses = Course.objects.actives()

    # bölgeleri ders, hoca ve sınıf kısıtlarına göre dolduruyoruz.

    for course in courses:
        values = [(int(instructor.id), int(room.id), int(day.id), hour)
                    # bu dersi verebileceğini söyleyen hocalar
                    for instructor in course.instructors.filter(is_active=True)
                        # bu ders için kapasite ve classroomtype uyanlar 
                        for room in ClassRoom.objects.filter(is_active=True, type__in=course.classroomtypes.all(),
                                                       capacity__gte=course.capacity)
                            for day in course.days.all()
                                for hour in range(9, 19-course.duration)]
        domains[course] = fd.FiniteDomain(values)

   
    ''' eğitmen çakışması da olmasın '''
    _courses = Course.objects.actives()
    for c1 in _courses:
        for c2 in _courses:
            if c1 != c2:
                c = NoInstructorClashConstraint((c1, c2))
                constraints.append(c)



    # constraint uygulama kısımları buradan itibaren başlıyor
    '''
        aynı döneme ait zorunlu dersler çakışamaz
    '''
    for i in range(1,9):
        _courses = Course.objects.actives().filter(terms__in=[i], mandatory=True)
        for c1 in _courses:
            for c2 in _courses:
                if c1 != c2:
                    c = MandatoryCourseClashConstraint((c1, c2))
                    constraints.append(c)

    '''
        tek ve çift dönemlere ait zorunlu dersler kendi aralarında çakışamaz
    '''
        
    for termgroup in ([1,3,5,7], [2,4,6,8]):
        _courses = Course.objects.actives().filter(terms__in=termgroup, mandatory=True)
        for c1 in _courses:
            for c2 in _courses:
                if c2 != c1:
                    c = TermConflictConstraint((c1, c2))
                    constraints.append(c)

    #'''
    #    aynı gün saat ve sınıfta iki ayrı ders olamaz
    #'''

    for c1 in Course.objects.actives():
        for c2 in courses:
            if c1 != c2:
                c = SameDaySameRoomConstraint((c1, c2))
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
