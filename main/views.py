# coding:utf-8 

from utils import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import *
from django.shortcuts import get_object_or_404
from utils.constraints import *
from django.contrib.auth import login as _login, logout as _logout, authenticate
from main.decorators import * 
from django.core.urlresolvers import reverse

objects = {
    'course': Course,
    'instructor': Instructor,
    'classroom': ClassRoom,
    'classroomtype': ClassRoomType
}

oforms = {
    'course': CourseForm,
    'instructor': InstructorForm,
    'classroom': ClassRoomForm,
    'classroomtype': ClassRoomTypeForm
}


@requires_login
def index(request):
    ''' burası tüm listenin görüneceği yer '''

    print request.user

    vtype = request.GET.get('view', 'course')
    sch = None
    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        pass 

    return render_to_response('index.jinja', locals())

@requires_login
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

    '''
        aynı gün saat ve sınıfta iki ayrı ders olamaz
    '''

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

    return HttpResponse('OK')


@requires_login
def addObject(request, objtype):
    _form = oforms.get(objtype)
    form = _form()
    op = u'add'

    if request.method == 'POST':
        form = _form(request.POST)
        if form.is_valid():
            obj = form.save()
            #return HttpResponse(cjson.encode(obj.to_dict()))
    #return HttpResponse('FAIL')
    return render_to_response('form.jinja', locals())
    

@requires_login
def editObject(request, objtype, objid):
    _obj = objects.get(objtype)
    _form = oforms.get(objtype)
    op = u'edit'

    obj = get_object_or_404(_obj, id=objid)
    form = _form(instance=obj)
    if request.method == 'POST':
        form = _form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            #return HttpResponse(cjson.encode(obj.to_dict()))
    return render_to_response('form.jinja', locals())

@requires_anonymous
def login(request):
    loginform = LoginForm()
    next = request.COOKIES.get('next', '/')

    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            d = loginform.cleaned_data 
            user = authenticate(username=d.get('user'), password=d.get('password'))

            if user:
                _login(request, user)
                response = HttpResponseRedirect(next)
                response.delete_cookie('next')
                return response

    return render_to_response('login.jinja', locals())

@requires_login
def logout(request):
    _logout(request)
    return HttpResponseRedirect(reverse('login'))

@requires_login
def list_items(request, item):
    idict = {
        'course': Course,
        'classroomtype': ClassRoomType,
        'instructor': Instructor,
        'classroom': ClassRoom
    }

    items = idict.get(item).objects.all()
    return render_to_response('list_items.jinja', locals())
