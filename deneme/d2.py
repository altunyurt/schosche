#coding:utf-8
import sys, os
p = "/home/den/calisma/python/schosche/"
sys.path.extend([ p, os.path.normpath(os.path.join(p, '..'))])
os.environ['DJANGO_SETTINGS_MODULE'] = 'schosche.settings'

from main.models import Course 
from utils.constraints import *

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

oddtermscourses = Course.objects.filter(terms__in=[1,3,5,7])
eventermscourses = Course.objects.filter(terms__in=[2,4,6,8])

for course1 in oddtermscourses:
    for course2 in oddtermscourses:
        if course1 != course2:
            c = TermConflictConstraint((course1, course2))
            constraints.append(c)

for course1 in eventermscourses:
    for course2 in eventermscourses:
        print course2, course1
        if course1 != course2:
            c = TermConflictConstraint((course1, course2))
            constraints.append(c)


r = Repository(courses, domains, constraints)
s = Solver()
s.distrib_cnt = 0
s.max_depth = 0
s.verbose = 0
x = s._solve(r)
print x.next()

