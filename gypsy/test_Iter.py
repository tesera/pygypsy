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

from GYPSYNonSpatial import densityAw




sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]


#bhage_Aw = 96

#BAincIter_Aw(sp_Aw, 0.05, 2.53, 37, 13.7, 100, 150, 96, printWarnings = True)
#sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw

#BA_Aw = numpy.linspace(1,50)
print BasalAreaIncrementNonSpatialAw('Aw', 0.37, 8.1, 112 ,124, 126, 4.56)


'''bhage is the parameter that changes considerably Aspen's BAinc curve '''


#pylab.plot(BA_Aw,y)

'''
BA_Sb = numpy.linspace(1,50)
y =  BasalAreaIncrementNonSpatialSb('Sb', 0.37, 8.07738602905, 112.98991932, 124.028786646, 126.963637205, BA_Sb)


pylab.plot(BA_Sb,y)


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