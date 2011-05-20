#coding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^\?view=(?P<vtype>instructor|course|room)', 'index', name='view_type'),
    

    # yeni nesne ekle
    url('^add/course/$', 'addObject', {'objtype':'course'}, name='addCourse'),
    url('^add/instructor/$', 'addObject', {'objtype':'instructor'}, name='addInstructor'),
    url('^add/classroom/$', 'addObject', {'objtype':'classroom'}, name='addClassRoom'),
    url('^add/classroomtype/$', 'addObject', {'objtype':'classroomtype'}, name='addClassRoomType'),

    # nesneleri düzenle
    url('^edit/course/(?P<objid>\d+)/$', 'editObject', {'objtype':'course'}, name='editCourse'),
    url('^edit/instructor/(?P<objid>\d+)/$', 'editObject', {'objtype':'instructor'}, name='editInstructor'),
    url('^edit/classroom/(?P<objid>\d+)/$', 'editObject', {'objtype':'classroom'}, name='editClassRoom'),
    url('^edit/classroomtype/(?P<objid>\d+)/$', 'editObject', {'objtype':'classroomtype'}, name='editClassRoomType'),

    url('^courses/$', 'list_items',  {'item':'course'}, name="courses"),
    url('^classroomtypes/$', 'list_items', {'item':'classroomtype'},  name="classroomtypes"),
    url('^instructors/$', 'list_items', {'item':'instructor'},  name="instructors"),
    url('^rooms/$', 'list_items', {'item':'classroom'},  name="classrooms"),


    url('^runconstraints/$','runconstraints', name='runconstraints'),

    url('^logout/$', 'logout', name="logout"),
    url('^login/$', 'login', name="login"),
)
