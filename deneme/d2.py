#coding:utf-8
import sys, os
p = "/home/den/calisma/python/schosche/"
sys.path.extend([ p, os.path.normpath(os.path.join(p, '..'))])
os.environ['DJANGO_SETTINGS_MODULE'] = 'schosche.settings'

from main.models import *
from utils.constraints import *
import hotshot 

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
