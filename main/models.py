# coding:utf-8 
from django.db import models
from django.forms.models import model_to_dict
import cjson 

'''
    modeller ve modeller içindeki basit kısıtlar domainleri oluşturmaya yarayacak.
    domainler oluştuktan sonra da genel kısıtlar söz konusu olacak

'''

class MyModel(models.Model):

    class Meta:
        abstract = True

    def to_dict(self):
        d = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        d.update(model_to_dict(self, fields=[field.name for field in self._meta.many_to_many]))
        return d


class JSONField(models.TextField):
    """DictField is a textfield that contains JSON-serialized dictionaries."""
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        value = cjson.decode(value)
        return value
    
    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""
        value = cjson.encode(value)
        return super(JSONField, self).get_db_prep_save(value)


class Term(MyModel):
    ''' Dönemler, yaz dönemi falan da eklenebilir. Tam olarak oturmadı kafamda dönem
    ve ders ilişkisi. Mesela döneminin dışında açılan derslerde neyapıyoruz?'''
    name = models.CharField(max_length=100, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s' % self.name 


class Day(MyModel):
    ''' Hafta günleri, belki ilerde cumartesi pazar falan da katılabilir.'''
    name = models.CharField(max_length=10, blank=False, unique=True)

    def __unicode__(self):
        return u'%s' % self.name 


class ClassRoomType(MyModel):
    ''' Sınıf tipleri, amfi, videolu ıvır kıvır.'''
    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % self.name 


class ClassRoom(MyModel):
    ''' Derslerin yapılacağı sınıflar. Sınıfın türü ve kapasitesi önemli'''
    name = models.CharField(max_length=10, null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(blank=False, null=False)
    type = models.ForeignKey(ClassRoomType)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.name


class CourseManager(models.Manager):
    def actives(self):
        qs = super(CourseManager, self).get_query_set()
        return qs.filter(is_active=True)



class Course(MyModel):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    code = models.CharField(max_length=15,  null=True, blank=True, unique=True)
    crn = models.CharField(max_length=15,  null=True, blank=True, unique=True)
    duration = models.PositiveSmallIntegerField(blank=False)
    mandatory = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    capacity = models.PositiveSmallIntegerField(null=False, blank=False)
    '''
        bu kısımda temel kısıtlar mevcut 
    ''' 
    days = models.ManyToManyField(Day, blank=True, null=True)
    terms = models.ManyToManyField(Term)
    classroomtypes = models.ManyToManyField(ClassRoomType, blank=True, null=True)

    objects = CourseManager()

    def __unicode__(self):
        return u'%s' % self.name 


class Instructor(MyModel):
    ''' Hocalar ve tercih ettikleri ders tipleri '''
    name = models.CharField(max_length=255, blank=False, null=False)
    preferred_courses = models.ManyToManyField('Course', related_name="instructors")
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.name 

class Schedule(MyModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    data = JSONField(blank=False, null=False)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name 
