#coding:utf-8
from constraint import * 

'''
    domainler
    ----------
    dönemler[1,2,3,4,5,6,7,8]
    günler [p,s,c,p,c]
    saatler [9, 16]
    hocalar [n] 
    dersler [m] zorunlu, dönem, saatler, çapraz
    sınıflar [t]
'''


p = Problem()
p.addVariable('donem', range(1,9))
p.addVariable('gun', ['pts', 'sali', 'cars', 'pers', 'cuma'])
p.addVariable('saat', range(9,19))
p.addVariable('hoca', ['ahmet', 'mehmet', 'hasan', 'huseyin', 'ayse', 'fatma', 'gulru', 'neslihan'])
p.addVariable('ders', ['ders1', 'ders2', 'ders3', 'ders4', 'ders5', 'ders6', 'ders7'])
p.addVariable('sinif', ['sinif1', 'sinif2', 'sinif3', 'sinif4'])





print p.getSolutions()


