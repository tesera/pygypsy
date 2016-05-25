# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:13:53 2016

@author: juliannosambatti
"""
import numpy
from asaCompileAgeGivenSpSiHt import computeTreeAge
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex

from GYPSYNonSpatial import densityNonSpatialAw
from GYPSYNonSpatial import densityNonSpatialSb
from GYPSYNonSpatial import densityNonSpatialSw
from GYPSYNonSpatial import densityNonSpatialPl

from GYPSYNonSpatial import densityAw

import matpRE: GYPSYlotlib.pyplot as plt


sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

N_Aw =  30.0
SI_bh_Aw = 4.46875150435
bhage_Aw = 10.0



y_Aw=densityNonSpatialAw (sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings = True)
SDF_Aw0 = y_Aw[1]
N_bh_Aw=y_Aw[0]
        
print  'N_bh_Aw = ', N_bh_Aw


'''

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