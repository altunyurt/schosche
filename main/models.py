# coding:utf-8 
from django.db import models
from django.forms.models import model_to_dict

'''
    modeller ve modeller içindeki basit kısıtlar domainleri oluşturmaya yarayacak.
    domainler oluştuktan sonra da genel kısıtlar söz konusu olacak

'''

class MyModel(models.Model):
    def to_dict(self):
        d = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        d.update(model_to_dict(self, fields=[field.name for field in self._meta.many_to_many]))
        return d


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
    is_usable = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.name


class CourseType(MyModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return u'%s' % self.name


class Lecturer(MyModel):
    ''' Hocalar ve tercih ettikleri ders tipleri '''
    name = models.CharField(max_length=255, blank=False, null=False)
    types = models.ManyToManyField(CourseType)

    def __unicode__(self):
        return u'%s' % self.name 

class Course(MyModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    duration = models.PositiveSmallIntegerField(blank=False)
    type = models.ForeignKey(CourseType, blank=False, null=False)
    mandatory = models.BooleanField(default=False)
    '''
        bu kısımda temel kısıtlar mevcut 
    ''' 
    days = models.ManyToManyField(Day, blank=True, null=True)
    terms = models.ManyToManyField(Term)
    rooms = models.ManyToManyField('ClassRoom', blank=True, null=True)


    def __unicode__(self):
        return u'%s' % self.name 


