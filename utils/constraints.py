# coding:utf-8

from __future__ import with_statement
import os 
#os.environ.update({'NO_PSYCO': ""})

from logilab.constraint import *
from logilab.constraint.propagation import AbstractConstraint, ConsistencyFailure


class SameDaySameRoomConstraint(AbstractConstraint):
    ''' A class can not have two or more courses registered on the same day same hours'''
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)


    def narrow(self, domains):
        _course1 = self._variables[0]
        course1 = dict(_course1)
        dom1 = domains[_course1]
        values1 = dom1.getValues()
        _course2 = self._variables[1]
        course2 = dict(_course2)
        dom2 = domains[_course2]
        values2 = dom2.getValues()

           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
        ''' main loop for each variable, the domain values are compared. values are kept in or removed
        from the domains according to the rules of the constraint'''
        for val1 in values1:
            instructor1, room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1["duration"]

            for val2 in values2:
                
                instructor2, room2, day2, hour2 = val2

                if room1 != room2 or day1 != day2:
                    keep1[val1] = keep2[val2] = 1

                elif not (val1 in keep1 and val2 in keep2 and maybe_entailed == 0):

                    start2, end2 = hour2, hour2 + course2["duration"]

                    if set(range(start1, end1)).intersection(set(range(start2, end2))):
                            maybe_entailed = 0

                    else:
                        keep1[val1] = 1
                        keep2[val2] = 1

        try:
            ''' non matching values are removed from the domains, leaving a reduced domain for further
            operations'''
            dom1.removeValues(set(values1).difference(keep1.keys()))
            dom2.removeValues(set(values2).difference(keep2.keys()))
        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            raise 
        return maybe_entailed


class MandatoryCourseClashConstraint(AbstractConstraint):
    '''
        Mandatory courses of given term must not clash
    '''
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)


    def narrow(self, domains):
        _course1 = self._variables[0]
        course1 = dict(_course1)
        dom1 = domains[_course1]
        values1 = dom1.getValues()
        _course2 = self._variables[1]
        course2 = dict(_course2)
        dom2 = domains[_course2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
    
        for val1 in values1:
            instructor1, room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1["duration"]

            for val2 in values2:

                instructor2, room2, day2, hour2 = val2
                if day1 != day2:
                    keep1[val1] = keep2[val2] = 1
                
                elif not ( val1 in keep1 and val2 in keep2 and maybe_entailed == 0):

                    start2, end2 = hour2, hour2 + course2["duration"]

                    ''' saatler ve günler çakışmamalı'''
                    if set(range(start1, end1)).intersection(set(range(start2, end2))):
                            maybe_entailed = 0

                    else:
                        keep1[val1] = 1
                        keep2[val2] = 1

        try:
            dom1.removeValues(set(values1).difference(keep1.keys()))
            dom2.removeValues(set(values2).difference(keep2.keys()))
        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise 
        return maybe_entailed
            


class TermConflictConstraint(AbstractConstraint):
    ''' mandatory courses of the given termgroups must not clash'''
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)
    

    def narrow(self, domains):
        _course1 = self._variables[0]
        course1 = dict(_course1)
        dom1 = domains[_course1]
        values1 = dom1.getValues()
        _course2 = self._variables[1]
        course2 = dict(_course2)
        dom2 = domains[_course2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
  
        for val1 in values1:
            instructor1, room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1["duration"]

            for val2 in values2:
                
                instructor2, room2, day2, hour2 = val2

                if day1 != day2:
                    keep1[val1] = keep2[val2] = 1

                elif not (val1 in keep1 and val2 in keep2 and maybe_entailed == 0):

                    start2, end2 = hour2, hour2 + course2["duration"]

                    if set(range(start1, end1)).intersection(set(range(start2, end2))):
                            maybe_entailed = 0

                    else:
                        keep1[val1] = keep2[val2] = 1

        try:
            dom1.removeValues(set(values1).difference(keep1.keys()))
            dom2.removeValues(set(values2).difference(keep2.keys()))

        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise 
        return maybe_entailed


class NoInstructorClashConstraint(AbstractConstraint):
    ''' An Instructor can not be at two courses at one time'''
    def __init__(self, courses):
        AbstractConstraint.__init__(self, courses)

    #@profile
    def narrow(self, domains):
        _course1 = self._variables[0]
        course1 = dict(_course1)
        dom1 = domains[_course1]
        values1 = dom1.getValues()
        _course2 = self._variables[1]
        course2 = dict(_course2)
        dom2 = domains[_course2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
  
        for val1 in values1:
            instructor1, room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + course1["duration"]

            for val2 in values2:

                instructor2, room2, day2, hour2 = val2
                if instructor1 != instructor2 or day1 != day2:
                    keep1[val1] = keep2[val2] = 1
                
                elif not (val1 in keep1 and val2 in keep2 and maybe_entailed == 0):

                    start2, end2 = hour2, hour2 + course2["duration"]

                    if set(range(start1, end1)).intersection(set(range(start2, end2))):
                            maybe_entailed = 0

                    else:
                        keep1[val1] = keep2[val2] = 1

        try:
            dom1.removeValues(set(values1).difference(keep1.keys()))
            dom2.removeValues(set(values2).difference(keep2.keys()))

        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise 
        return maybe_entailed
