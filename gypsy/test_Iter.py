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


sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]


'''
N_Aw =  136.87753732
SI_bh_Aw = 4.46875150435
bhage_Aw = 427.214334144



y_Aw=densityNonSpatialAw (sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings = True)
SDF_Aw0 = y_Aw[1]
N_bh_Aw=y_Aw[0]
        
print  'N_bh_Aw = ', N_bh_Aw

x = numpy.arange(5.0, 200, 5.0)
#print x

N_Aw = 100.0
#SDF_Aw0 = 10.0
SI_bh_Aw = 4.2
bhage_Aw = 35.0

   
SDF_Aw0 = N_Aw

c0=0.717966
c1=6.67468
b3=(1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)

b2=(c0/4)*((SDF_Aw0**0.5)**(1/SDF_Aw0))

b1=( (1/((SDF_Aw0/1000)**(0.5)) ) + (numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1))))) ) * numpy.log(50+1)
k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(bhage_Aw)))

#b1=( (1/((SDF_Aw0/1000)**(0.5)) ) + (numpy.sqrt(1+numpy.sqrt(bhage_Aw/(numpy.sqrt(SDF_Aw0)*numpy.log(bhage_Aw+1))))) ) * numpy.log(bhage_Aw+1)
#k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(bhage_Aw+1)))
#k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(bhage_Aw)))

SDF_Aw1 = N_Aw * k2/k1


N_Aw1 = SDF_Aw1 * k1/k2


print SDF_Aw1, N_Aw1

SDF_Aw0 = SDF_Aw1

b3=(1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)

b2=(c0/4)*((SDF_Aw0**0.5)**(1/SDF_Aw0))

b1=( (1/((SDF_Aw0/1000)**(0.5)) ) + (numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1))))) ) * numpy.log(50+1)
k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50)))



N_50 = SDF_Aw0 * k1/k2

print N_50 

SDF_Aw0 = 37.0

c0=0.717966
c1=6.67468
b3=(1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)

b2=(c0/4)*((SDF_Aw0**0.5)**(1/SDF_Aw0))

b1=( (1/((SDF_Aw0/1000)**(0.5)) ) + (numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1))))) ) * numpy.log(50+1)
k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(bhage_Aw)))



N_20 = SDF_Aw0 * k1/k2

print N_20 

'''

from scipy.optimize import fmin

N_Aw = 100.0
#SDF_Aw0 = 10.0
SI_bh_Aw = 4.2
bhage_Aw = 35.0

#y_Aw = densityAw  (SDF_Aw, bhage_Aw, SI_bh_Aw)


x0 = [200.0]

#print y_Aw



optimize = fmin (densityAw, x0 , args = (bhage_Aw, SI_bh_Aw))

'''

print densityAw  (N, bhage_Aw, SI_bh_Aw)

for i in x:
    N_Aw = 136
    #SDF_Aw0 = 10.0
    SI_bh_Aw = 4.2
    bhage_Aw = 21
    
    y_Aw=densityAw  (i, bhage_Aw, SI_bh_Aw)
    print i, y_Aw
    
       

N_Sb =  136.87753732
SI_bh_Sb = 7.36406861253
tage_Sb = 150

y_Sb=densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb)
SDF_Sb0 = y_Sb[1]
N_bh_Sb=y_Sb[0]

#print  'N_bh_Sb = ', N_bh_Sb
#print 'SDF_Sb =  ', SDF_Sb0


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