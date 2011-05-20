# coding:utf-8 
from django.db import models
from django.forms.models import model_to_dict
import cjson 

'''
    modeller ve modeller içindeki basit kısıtlar domainleri oluşturmaya yarayacak.
    domainler oluştuktan sonra da genel kısıtlar söz konusu olacak

'''

class QuerySetManager(models.Manager):
    def get_query_set(self):
        ''' modele özgü queryset kullanılıyor '''
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
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=u"Derslik tipi")

    def __unicode__(self):
        return u'%s' % self.name 


class ClassRoom(MyModel):
    ''' Derslerin yapılacağı sınıflar. Sınıfın türü ve kapasitesi önemli'''
    name = models.CharField(max_length=10, null=False, blank=False, verbose_name=u"Derslik adı")
    capacity = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name=u"Öğrenci sayısı")
    type = models.ForeignKey(ClassRoomType, verbose_name=u"Derslik tipi")
    is_active = models.BooleanField(default=True, verbose_name=u"Kullanılabilir")

    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        def actives(self):
            return self.filter(is_active=True)

    def __unicode__(self):
        return u'%s' % self.name


class Course(MyModel):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name=u"Ders adı")
    code = models.CharField(max_length=15,  null=True, blank=True, unique=True, verbose_name=u"Ders kodu")
    crn = models.CharField(max_length=15,  null=True, blank=True, unique=True)
    duration = models.PositiveSmallIntegerField(blank=False, verbose_name=u"Süre")
    mandatory = models.BooleanField(default=False, verbose_name=u"Zorunlu ders")
    is_active = models.BooleanField(default=True, verbose_name=u"Ders aktif")
    capacity = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u"Öğrenci sayısı")
    '''
        bu kısımda temel kısıtlar mevcut 
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
    ''' Hocalar ve tercih ettikleri ders tipleri '''
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
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    data = JSONField(blank=False, null=False)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name 
