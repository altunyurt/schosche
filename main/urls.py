from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url('^$', 'index', name='index'),

    # yeni nesne ekle
    url('^add/course/$', 'addObject', {'objtype':'course'}, name='addCourse'),
    url('^add/lecturer/$', 'addObject', {'objtype':'lecturer'}, name='addLecturer'),
    url('^add/coursetype/$', 'addObject', {'objtype':'coursetype'}, name='addCourseType'),
    url('^add/classroom/$', 'addObject', {'objtype':'classroom'}, name='addClassRoom'),
    url('^add/classroomtype/$', 'addObject', {'objtype':'classroomtype'}, name='addClassRoomType'),

    # nesneleri düzenle
    url('^edit/course/(?P<objid>\d+)/$', 'editObject', {'objtype':'course'}, name='editCourse'),
    url('^edit/lecturer/(?P<objid>\d+)/$', 'editObject', {'objtype':'lecturer'}, name='editLecturer'),
    url('^edit/coursetype/(?P<objid>\d+)/$', 'editObject', {'objtype':'coursetype'}, name='editCourseType'),
    url('^edit/classroom/(?P<objid>\d+)/$', 'editObject', {'objtype':'classroom'}, name='editClassRoom'),
    url('^edit/classroomtype/(?P<objid>\d+)/$', 'editObject', {'objtype':'classroomtype'}, name='editClassRoomType'),
)
