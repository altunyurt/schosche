#coding:utf-8
import sys, os
p = "/home/den/calisma/python/schosche/"
sys.path.extend([ p, os.path.normpath(os.path.join(p, '..'))])
os.environ['DJANGO_SETTINGS_MODULE'] = 'schosche.settings'

from main.models import *
from utils.constraints import *


domains = {}
constraints = []

''' her ders için zaten veri girişind uygulanan kısıtlara göre domain oluştur'''
courses = Course.objects.actives()

# bölgeleri ders, hoca ve sınıf kısıtlarına göre dolduruyoruz.

fcourses = []
fscourses = []

def mfs(d):
    items = d.items()
    t = tuple((key,isinstance(val, list) and tuple(val) or val) for key, val in items)
    return frozenset(t)



for course in courses:
    values = [(int(instructor.id), int(room.id), int(day.id), hour)
                # bu dersi verebileceğini söyleyen hocalar
                for instructor in Instructor.objects.all()
                    # bu ders için kapasite ve classroomtype uyanlar 
                    for room in ClassRoom.objects.filter(is_active=True, type__in=course.classroomtypes.all(),
                                                   capacity__gte=course.capacity)
                        for day in course.days.all()
                            for hour in range(9, 19-course.duration)]
    d= course.to_dict()
    fcourse = mfs(d)
    domains[fcourse] = fd.FiniteDomain(values)
    fscourses.append(fcourse)
    fcourses.append(d)



''' eğitmen çakışması da olmasın '''
for c1 in fcourses:
    for c2 in fcourses:
        if c1 != c2:
            c = NoInstructorClashConstraint((mfs(c1), mfs(c2)))
            constraints.append(c)

            c = SameDaySameRoomConstraint((mfs(c1), mfs(c2)))
            constraints.append(c)



# constraint uygulama kısımları buradan itibaren başlıyor
'''
    aynı döneme ait zorunlu dersler çakışamaz
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
    tek ve çift dönemlere ait zorunlu dersler kendi aralarında çakışamaz
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


r = Repository(fscourses, domains, constraints)
s = Solver()
s.distrib_cnt = 0
s.max_depth = 0
s.verbose = 0
x = s._solve(r)
print x.next()
