# coding:utf-8 
from django.db import models
from django.forms.models import model_to_dict
import cjson 
import cPickle as cp
from cStringIO import StringIO


class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)


class MyModel(models.Model):

    class Meta:
        abstract = True

    def to_dict(self):
        d = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        d.update(model_to_dict(self, fields=[field.name for field in self._meta.many_to_many]))
        return d


class JSONField(models.TextField):
    '''DictField is a textfield that contains JSON-serialized dictionaries.'''
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        '''Convert our string value to JSON after we load it from the DB'''
        value = cjson.decode(value)
        return value
    
    def get_db_prep_save(self, value):
        '''Convert our JSON object to a string before we save'''
        value = cjson.encode(value)
        return super(JSONField, self).get_db_prep_save(value)


class Term(MyModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s' % self.name 


class Day(MyModel):
    ''' Week days '''
    name = models.CharField(max_length=10, blank=False, unique=True)

    def __unicode__(self):
        return u'%s' % self.name 


class ClassRoomType(MyModel):
    ''' Types of the clasrooms. Might be used to better select the domains if for example a course 
    requires a classand another needs a laboratory'''
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=u"Derslik tipi")

    def __unicode__(self):
        return u'%s' % self.name 


class ClassRoom(MyModel):
    ''' ClassRoom object. Courses are directly related to clasrooms via course student limits and
    classroomtypes.'''
    name = models.CharField(max_length=10, null=False, blank=False, verbose_name=u"Derslik adı")
    capacity = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name=u"Öğrenci sayısı")
    type = models.ForeignKey(ClassRoomType, verbose_name=u"Derslik tipi")
    is_active = models.BooleanField(default=True, verbose_name=u"Kullanılabilir")

    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        def actives(self):
            ''' return usable classrooms'''
            return self.filter(is_active=True)

    def __unicode__(self):
        return u'%s' % self.name


class Course(MyModel):
    ''' course data object. '''
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name=u"Ders adı")
    code = models.CharField(max_length=15,  null=True, blank=True, unique=True, verbose_name=u"Ders kodu")
    crn = models.CharField(max_length=15,  null=True, blank=True, unique=True)
    duration = models.PositiveSmallIntegerField(blank=False, verbose_name=u"Süre")
    mandatory = models.BooleanField(default=False, verbose_name=u"Zorunlu ders")
    is_active = models.BooleanField(default=True, verbose_name=u"Ders aktif")
    capacity = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u"Öğrenci sayısı")
    '''
        basic constraints. these are not used in constraint satisfaction problem directly, but used in 
        filling up the value domains for the variables(courses), which results in lesser runtime 
    ''' 
    days = models.ManyToManyField(Day, blank=True, null=True, verbose_name=u"Günler")
    terms = models.ManyToManyField(Term, verbose_name=u"Dönemler")
    classroomtypes = models.ManyToManyField(ClassRoomType, blank=True, null=True, 
                                            verbose_name=u"Derslik tipleri")

    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        ''' queryseti bir miktar değiştirmek gerekti actives mevzuu için'''
        def actives(self):
            return self.filter(is_active=True)
    
        def as_dicts(self):
            return [item.to_dict() for item in self._clone()]
                
        def as_hashables(self):
            ds = self.as_dicts()
            l = []
            for course in ds:
                f = frozenset((item[0],isinstance(item[1], list) and tuple(item[1]) or item[1]) \
                    for item in course.items())
                l.append(f)
            return l



    def __unicode__(self):
        return u'%s' % self.name 


class Instructor(MyModel):
    ''' Instructor data object. Here we can chose if instructor prefers several different courses, which helps 
    returning better solutions by not making unrelated matches between courses and instructors of different
    areas'''
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name=u"Eğitmen adı")
    preferred_courses = models.ManyToManyField('Course', related_name="instructors", verbose_name=u"Tercih edilen dersler")
    is_active = models.BooleanField(default=True, verbose_name=u"Eğitmen aktif")

    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        def actives(self):
            return self.filter(is_active=True)

    def __unicode__(self):
        return u'%s' % self.name 


class Schedule(MyModel):
    ''' timetable data object. there may be several records but only the default one be displayed'''
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    data = JSONField(blank=False, null=False)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name 

    def get_unpickled(self):
        ''' returns the converted object data upon fetching from database '''
        flike = StringIO()
        flike.write(self.data)
        flike.seek(0)

        return  cp.load(flike)


