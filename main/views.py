# coding:utf-8 

from utils import render_to_response, mfs
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
    ''' main view where the default solution is displayed as a timetable'''

    vtype = request.GET.get('view', 'course')
    sch = None
    try:
        sch = Schedule.objects.get(is_default=True)
    except:
        pass 

    return render_to_response('index.jinja', locals())


@requires_login
def runconstraints(request):
    '''
        Constraint application is called by web user directly.
    '''
    domains = {}
    constraints = []

    courses = Course.objects.actives()

    fcourses = []
    fscourses = []


    '''
        domains are created by chosing the possible values visely at the beginning. 
        Reason here is to reduce the runtime, for the constraint solver will be looping 
        over the combinations of variables and values, which is the real time taking process.
        Reducing the possible values will also result in reducingthe runtime and memory allocated.
    
    '''
    for course in courses:
        values = [(int(instructor.id), int(room.id), int(day.id), hour)
                    for instructor in course.instructors.actives()
                        # bu ders için kapasite ve classroomtype uyanlar 
                        for room in ClassRoom.objects.actives().filter(type__in=course.classroomtypes.all(),
                                                       capacity__gte=course.capacity)
                            for day in course.days.all()
                                for hour in range(9, 19-course.duration)]
        d= course.to_dict()
        fcourse = mfs(d)
        domains[fcourse] = fd.FiniteDomain(values)
        fscourses.append(fcourse)
        fcourses.append(d)

   
    for c1 in fcourses:
        for c2 in fcourses:
            if c1 != c2:
                ''' we don't want to end up with results where an instructor 
                has two or more courses at the same time '''
                c = NoInstructorClashConstraint((mfs(c1), mfs(c2)))
                constraints.append(c)

                '''
                    No classrooms can have two or more courses registered at the same day, 
                    same hours
                '''

                c = SameDaySameRoomConstraint((mfs(c1), mfs(c2)))
                constraints.append(c)

    '''
        Mandatory courses of the each term should not be on the same day and same hours
    '''
    for i in range(1,9):
        for c1 in fcourses:
            if i not in c1.get('terms') or not c1.get('mandatory'):
                continue 
    
            for c2 in fcourses:
                if i not in c2.get('terms') or not c2.get('mandatory'):
                    continue 
    
                if c1 != c2:
                    c = MandatoryCourseClashConstraint((mfs(c1), mfs(c2)))
                    constraints.append(c)

    '''
        mandator courses of the terms [1,3,5,7] and [2,4,6,8] should not be on the same day, 
        same hours
    '''
        
    for termgroup in ([1,3,5,7], [2,4,6,8]):
        for c1 in fcourses:
    
            if not c1.get('mandatory') or not set(c1.get('terms')).intersection(termgroup):
                continue
    
            for c2 in fcourses:
                if not c2.get('mandatory') or not set(c2.get('terms')).intersection(termgroup):
                    continue
                if c2 != c1:
                    c = TermConflictConstraint((mfs(c1), mfs(c2)))
                    constraints.append(c)



    ''' Repository is the structure that stores the domains, variables and constraints, 
    propagates the domain changes to constraints and manages the constraint evaluation queue''' 
    r = Repository(fscourses, domains, constraints)
    ''' create a solver'''
    s = Solver()

    s.distrib_cnt = 0
    s.max_depth = 0
    s.verbose = 0
    ''' generate a solutution pointer for CSP'''
    x = s._solve(r)
    ''' get next solution from the solution space. this is the long running process'''
    solution = x.next()
    
    ''' when solutio found, we want to store it as a database document. for the solution is in 
    python dictionary format, we need to convert it into string data'''
    filelike = cStringIO.StringIO()
    cPickle.dump(solution, filelike)
    
    filelike.seek(0)
    data = cjson.encode(filelike.read())

    ''' saving the solution into database as string'''
    schedule = Schedule(name="Schedule1", data=data, is_default=True)
    schedule.save()

    return HttpResponse('OK')


@requires_login
def addObject(request, objtype):
    ''' general purpose data entry method.'''
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
    ''' general purpose data object editing method. '''
    _obj = objects.get(objtype)
    _form = oforms.get(objtype)
    op = u'edit'

    obj = get_object_or_404(_obj, id=objid)
    form = _form(instance=obj)
    if request.method == 'POST':
        form = _form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
    return render_to_response('form.jinja', locals())

@requires_anonymous
def login(request):
    ''' Authentication page. For anonymus users, this is the entry point to application. '''
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
    ''' sign user out'''
    _logout(request)
    return HttpResponseRedirect(reverse('login'))

@requires_login
def list_items(request, item):
    ''' General purpose listing page. Database records such as course, clasrooms, instructors 
    are listed via this method. User can view or edit the relevant objects by chosing them from this page.'''
    idict = {
        'course': Course,
        'classroomtype': ClassRoomType,
        'instructor': Instructor,
        'classroom': ClassRoom
    }

    items = idict.get(item).objects.all()
    return render_to_response('list_items.jinja', locals())
