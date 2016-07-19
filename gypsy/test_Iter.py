# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:13:53 2016

@author: juliannosambatti
"""
import numpy

import matplotlib
import matplotlib.pyplot as plt
import pylab

from asaCompileAgeGivenSpSiHt import computeTreeAge
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex

from GYPSYNonSpatial import densityNonSpatialAw
from GYPSYNonSpatial import densityNonSpatialSb
from GYPSYNonSpatial import densityNonSpatialSw
from GYPSYNonSpatial import densityNonSpatialPl

from GYPSYNonSpatial import BAincIter_Aw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialAw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSb
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialPl

from GYPSYNonSpatial import densityAw

from GYPSYNonSpatial import BAfactorFinder_Aw1
from GYPSYNonSpatial import BAfromZeroToDataAw
from GYPSYNonSpatial import BAfactorFinder_Sw
from GYPSYNonSpatial import BAfromZeroToDataSw

from GYPSYNonSpatial import BAfactorFinder_Sb
from GYPSYNonSpatial import BAfromZeroToDataSb

from GYPSYNonSpatial import BAfactorFinder_Pl1
from GYPSYNonSpatial import BAfromZeroToDataPl1


'''

sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]





#bhage_Aw = 96

#BAincIter_Aw(sp_Aw, 0.05, 2.53, 37, 13.7, 100, 150, 96, printWarnings = True)
#sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw

bhage_Aw = numpy.linspace(1,250)
y = BasalAreaIncrementNonSpatialAw('Aw', 1.0, 18, 112 ,124, 50, 30)

'''

x = BAfactorFinder_Aw1 (22.69440976, 22.69440976, 17.67132362, 0.0590343581173, 3.599599399, 108.126896, 108.1275845, 0.5, 0.78688416, printWarnings = True)

#y = BAfromZeroToDataAw (45.0750948321, 41.0, 8.67714804702, 0.695823185569, 7.38789213445, 817.46652306, 964.419885613, 7.57069610206, 0.3, simulation_choice)
print x

#pylab.plot(bhage_Aw,y)

'''
BA_Sb = numpy.linspace(1,50)
y =  BasalAreaIncrementNonSpatialSb('Sb', 0.37, 8.07738602905, 112.98991932, 124.028786646, 126.963637205, BA_Sb)

pylab.plot(BA_Sb,y)


 #sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw


#BA_Sw = numpy.linspace(1,250)
#y = BasalAreaIncrementNonSpatialSw('Sw', 0.30 , 16 , 192.083099398 , 20 , BA_Sw, 200, 100.0, 200.0 , 5) 


y = BAfromZeroToDataSw (55.264007984, 55.264007984, 14.3277198745, 0.0466314877955, 15, 47.7763759, 47.779382906, 0.0, 900.756683418, 0.0 ,0.375068155812, 0.33699327622, 'yes' )

#x = BAfactorFinder_Sw (55.264007984, 55.264007984, 14.3277198745, 0.0466314877955, 15, 47.7763759, 47.779382906, 0.0, 900.756683418, 0.0,0.375068155812, 0.43940595, printWarnings = True)

print y

#pylab.plot(BA_Sw,y)






f_Pl = numpy.linspace(1,50)


#y = BAfromZeroToDataPl1 (37.59, 24, 14.42, 0.89, 6.38, 1294, 1322, 159, 0.0, 0.0, 10.38, 4.26)

#pylab.plot(f_Pl,y)

x = BAfactorFinder_Pl1 (22.69, 22.69, 17.67, 0.06, 3.59, 108, 1, 159, 0.0, 0.0, 10.38, 14.78, printWarnings = True)

print x




y_Aw=densityNonSpatialAw (sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings = True)
SDF_Aw0 = y_Aw[1]
N_bh_Aw=y_Aw[0]
        
print  'N_bh_Aw = ', N_bh_Aw



x = numpy.arange(5.0, 200, 5.0)
print x
    

N_Sb =  136.87753732
SI_bh_Sb = 7.36406861253
tage_Sb = 150

y_Sb=densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb)
SDF_Sb0 = y_Sb[1]
N_bh_Sb=y_Sb[0]

print  'N_bh_Sb = ', N_bh_Sb
print 'SDF_Sb =  ', SDF_Sb0


N_Sw =  51.919065879999998
SI_bh_Sw = 5.87487436021
tage_Sw = 192

y_Sw= densityNonSpatialSw (sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw, N_Sw)
SDF_Sw0 = y_Sw[1]
N_bh_Sw=y_Sw[0]

#print  'N_bh_Sb = ', N_bh_Sb
#print 'SDF_Sb =  ', SDF_Sb0


N_Pl =  283
SI_bh_Pl = 7.19385720708
tage_Pl = 25

y_Pl =densityNonSpatialPl (sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw, SDF_Sw, SDF_Sb, N_Pl)
SDF_Pl0 = y_Pl[1]
N_bh_Pl = y_Pl[0]

#print  'N_bh_Pl = ', N_bh_Pl
#print 'SDF_Pl =  ', SDF_Pl0


x_Pl = densityPl  (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl , SI_bh_Pl)

#print x_Pl


Age_Aw = computeTreeAge(siSp='',treeHt = 20, treeSi=SI_bh_Aw, maxTreeAge = 450, rowIndex = 0, printWarnings = True)

''' 