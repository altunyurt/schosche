#coding:utf-8
from logilab.constraint import *
from pprint import pprint
from exceptions import Exception


class VarOlmError(Exception):
    pass

'''
    domainler
    ----------
    dönemler[1,2,3,4,5,6,7,8]
    günler [p,s,c,p,c]
    saatler [9, 16]
    hocalar [n] 
    dersler [m] zorunlu, dönem, saatler, çapraz
    sınıflar [t]

    problem 
    --------
    - aynı sınıfta iki ders olamaz.
    - aynı hoca aynı saatte iki ayrı sınıfta olamaz
    - dersler iki saatlik 


    derslerin iki saatlik olduğu belli değil. çözülmesi gereken problem şu aslında. 
    öncelikle dersler, hocalar, günler ve saatler var. sonra sınıflar gelecek, sonra




'''


ders =  ['ders1', 'ders2', 'ders3', 'ders4', 'ders5', 'ders6', 'ders7']
donem =  range(1,9)
gun =  ['pts', 'sali', 'cars', 'pers', 'cuma']
slot =  [(a,a+2) for a in range(9,17)]
hoca =  ['ahmet', 'mehmet', 'hasan', 'huseyin', 'ayse', 'fatma', 'gulru', 'neslihan']
sinif =  ['sinif1', 'sinif2', 'sinif3', 'sinif4']

''' 
    bu herif harici kısıtlara göre çalışıyor ya 
    birbirine göre kısıt nasıl koacağız mınkı

'''
courses = []


class Course(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                raise VarOlmError('%s varmış bu elemanda' % k)
            setattr(self, k, v)

    def __repr__(self):
        return u"<Course: %s by %s at %s on %s %s in term %s>" % (self.name, self.lecturer, self.room, self.day,
                                                       self.slot, self.term)


c = [Course(duration=3), Course(duration=2), Course(duration=1)] 
t = range(9,19)

class CantOverLapConstraint(Constraint):
    def __call__(self, variables, domains, assignments, forwardcheck=False,
                _unassigned=Unassigned):
        
        

p = Problem()
p.addVariables(c, t)
p.addConstraint(WhatIsThisConstraint())
print p.getSolution()
