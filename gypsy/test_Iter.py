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

from GYPSYNonSpatial import BAfactorFinder_Aw
from GYPSYNonSpatial import BAfromZeroToDataAw
from GYPSYNonSpatial import BAfactorFinder_Sw
from GYPSYNonSpatial import BAfromZeroToDataSw

from GYPSYNonSpatial import BAfactorFinder_Sb
from GYPSYNonSpatial import BAfromZeroToDataSb

from GYPSYNonSpatial import BAfactorFinder_Pl
from GYPSYNonSpatial import BAfromZeroToDataPl




sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]





#bhage_Aw = 96

#BAincIter_Aw(sp_Aw, 0.05, 2.53, 37, 13.7, 100, 150, 96, printWarnings = True)
#sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw
'''
bhage_Aw = numpy.linspace(1,250)
y = BasalAreaIncrementNonSpatialAw('Aw', 1.0, 18, 112 ,124, 50, 30)
'''

x = BAfactorFinder_Aw (135.882225194, 135.882225194, 7.91858798922, 0.388143801307, 8.07738602905, 112.7773209, 124.028786646, 0.973625975173, 6, printWarnings = True)

#y = BAfromZeroToDataAw (135.882225194, 135.882225194, 7.91858798922, 0.388143801307, 8.07738602905, 112.7773209, 124.028786646, 0.973625975173, 1.03)
print x

#pylab.plot(bhage_Aw,y)
'''

BA_Sb = numpy.linspace(1,50)
y =  BasalAreaIncrementNonSpatialSb('Sb', 0.37, 8.07738602905, 112.98991932, 124.028786646, 126.963637205, BA_Sb)

pylab.plot(BA_Sb,y)


 #sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw


#BA_Sw = numpy.linspace(1,250)
#y = BasalAreaIncrementNonSpatialSw('Sw', 0.30 , 16 , 192.083099398 , 20 , BA_Sw, 200, 100.0, 200.0 , 5) 



# y = BAfromZeroToDataSw (135.882225194, 106.0, 13.1761233942, 0.611856198693, 7.9834026698, 192.0262491, 195.51460482, 123.019252926, 0.0, 0.0, 1.53478964784, 0.956)

x = BAfactorFinder_Sw (135.882225194, 106.0, 13.1761233942, 0.611856198693, 7.9834026698, 192.0262491, 195.51460482, 123.019252926, 0.0, 0.0, 0.9, 20, printWarnings = True)

print x


pylab.plot(BA_Sw,y)



#

f_Pl = numpy.linspace(1,50)
y = BAfromZeroToDataPl (135.882225194, 106.0, 13.1761233942, 0.611856198693, 7.9834026698, 192.0262491, 195.51460482, 123.019252926, 0.0, 0.0, 0.9, 50)

#pylab.plot(f_Pl,y)

#x = BAfactorFinder_Pl (135.882225194, 106.0, 13.1761233942, 0.611856198693, 7.9834026698, 192.0262491, 195.51460482, 123.019252926, 0.0, 0.0, 0.9, 65, printWarnings = True)

print y




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