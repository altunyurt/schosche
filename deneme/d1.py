# coding:utf-8

import os 
os.environ.update({'NO_PSYCO': ""})
from logilab.constraint import * 
from logilab.constraint.propagation import AbstractConstraint, ConsistencyFailure
import random
import numpy as np
import cjson



class Course(object):
    def __init__(self, name, hours):
        self.hours = hours
        self.name = name 

    def __repr__(self):
        return u'<Course: %s>' % self.name

variables = [Course('c%02d' % (i + 1) , hours) for i,hours in enumerate((1,3,2,4,2))]#,3,4,3,2,3,4,5,6))]

random.shuffle(variables)

values = [(room,day, hour)
                for room in ('room A','room B', 'room C')
                for day in ('day 1', 'day 2', 'day 3', 'day 4')
                for hour in range(9, 19)
         ]

domains = {}
for v in variables:
    domains[v]=fd.FiniteDomain(values)

constraints = []
''' 
bu kısım yanlış. kaç ders olavağını bilmiyorum. "günü şu olanların" toplamı demek lazım
ibreti alem için kalsın 

for room in variables:
    for room2 in variables:
        for room3 in variables:
            if room3 not in (room2, room1) and room1 != room2:
                constraints.append(fd.make_expression((room1, room2, room3), )'

'''

class SameDaySameClassConstraint(AbstractConstraint):
    def __init__(self, variables):
        AbstractConstraint.__init__(self, variables)
    @profile 
    def narrow(self, domains):
        maybe_entailed = 1
        var1 = self._variables[0]
        dom1 = domains[var1]
        values1 = dom1.getValues()
        var2 = self._variables[1]
        dom2 = domains[var2]
        values2 = dom2.getValues()
           
        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
    
        for val1 in values1:
            
            room1, day1, hour1 = val1
            start1, end1 = hour1, hour1 + var1.hours

            for val2 in values2:
                
                if not (val1 in keep1 and val2 in keep2 and maybe_entailed == 0):

                    room2, day2, hour2 = val2
                    start2, end2 = hour2, hour2 + var2.hours

                    if room1 == room2 and day1 == day2 and \
                         set(range(start1, end1)).intersection(set(range(start2, end2))):
                            #print val1, val2, 'maybe entitled'
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
            raise 
        return maybe_entailed
            
        

for v1 in variables:
    for v2 in variables:
        if v1 != v2 :
            c = SameDaySameClassConstraint((v1, v2))
            constraints.append(c)


r = Repository(variables, domains, constraints)
s = Solver()
s.distrib_cnt = 0
s.max_depth = 0
s.verbose = 1
x = s._solve(r)
x.next()
