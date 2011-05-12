#coding:utf-8

from django.contrib import admin 
from main.models import *

class CourseAdmin(admin.ModelAdmin):
    pass

class CourseTypeAdmin(admin.ModelAdmin):
    pass

class DayAdmin(admin.ModelAdmin):
    pass

class TermAdmin(admin.ModelAdmin):
    pass

class ClassRoomAdmin(admin.ModelAdmin):
    pass

class ClassRoomTypeAdmin(admin.ModelAdmin):
    pass

class LecturerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(ClassRoomType, ClassRoomTypeAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Lecturer, LecturerAdmin)
