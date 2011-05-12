# coding:utf-8

from logilab.constraint import *
from logilab.constraint.propagation import AbstractConstraint, ConsistencyFailure

'''
    Genel kısıtlar. 
     - Dersler çakışan saatlerde aynı sınıfta yer alamaz
     - Aynı hoca çakışan saatlerde derslere giremez
     - 1,3,5,7 ve 2,4,6,8 dönem zorunlu dersleri aynı saatlere gelemez


'''



class SameDaySameRoomConstraint(AbstractConstraint):
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)

    def narrow(self, domains):
        maybe_entailed = 1
        course1 = self._variables[0]
        dom1 = domains[course1]
        values1 = dom1.getValues()
        course2 = self._variables[1]
        dom2 = domains[course2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
    
        for val1 in values1:
            
            room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1.hours

            for val2 in values2:
                
                if val1 in keep1 and val2 in keep2 and maybe_entailed == 0:
                    continue

                room2, day2, hour2 = val2
                start2, end2 = hour2, hour2 + course2.hours

                if room1 == room2 and day1 == day2 and \
                     set(range(start1, end1)).intersection(set(range(start2, end2))):
                        maybe_entailed = 0

                else:
                    keep1[val1] = 1
                    keep2[val2] = 1

        try:
            dom1.removeValues([val for val in values1 if val not in keep1])
            dom2.removeValues([val for val in values2 if val not in keep2])            
        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise 
        return maybe_entailed


class MandatoryCourseClashConstraint(AbstractConstraint):
    '''
        Aynı dönemin zorunlu dersleri aynı saatlere gelemez. Aslında 
        bu kısıt sadece saat ve gün çakışmasını kontrol ediyor. 
        Sadece değişkenleri aldığımız kümede seçimi dönemlere göre yapıyoruz.
        Yani 1,3,5,7 ve 2,4,6,8 dönemlerinden zorunlu dersleri alıp bunlara 
        birer kısıt koyuyoruz.
    
    '''
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)

    def narrow(self, domains):
        maybe_entailed = 1
        course1 = self._variables[0]
        dom1 = domains[course1]
        values1 = dom1.getValues()
        course2 = self._variables[1]
        dom2 = domains[course2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
    
        for val1 in values1:
            room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1.hours

            for val2 in values2:
                
                if val1 in keep1 and val2 in keep2 and maybe_entailed == 0:
                    continue

                room2, day2, hour2 = val2
                start2, end2 = hour2, hour2 + course2.hours

                if room1 == room2 and day1 == day2 and \
                     set(range(start1, end1)).intersection(set(range(start2, end2))):
                        maybe_entailed = 0

                else:
                    keep1[val1] = 1
                    keep2[val2] = 1

        try:
            dom1.removeValues([val for val in values1 if val not in keep1])
            dom2.removeValues([val for val in values2 if val not in keep2])            
        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise 
        return maybe_entailed
            
 
