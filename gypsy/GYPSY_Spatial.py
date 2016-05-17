# -*- coding: utf-8 -*-
""" Functions 
Created on Wed Apr  6 08:20:38 2016

@author: juliannosambatti
"""

import numpy
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge


"""
estimating Sit, total age, and bhage using asaCompileAgeGivenSpSiHt functions
"""
# input - species, top height, total age, BH age, N (or density), current Basal Area, Measured Percent Stocking, StumpDOB, StumpHeight, TopDib
sp_Aw=['Aw', 25, 60, 56, 1000, 50, 16.9, 13, 0.3, 7, 0]
sp_Sb=['Sb', 20, 70, 66, 1000, 50, 11.7, 13, 0.3, 7, 0]
sp_Pl=['Pl', 20, 80, 76, 1000, 50, 83.8, 13, 0.3, 7, 0]
sp_Sw=['Sw', 20, 90, 86, 1000, 50, 28.9, 13, 0.3, 7, 0]

'''
b_hage = Breast Height Age
tage = Total age

the algorithm accepts either one

si_Aw  =  estimated Site intex according to the paper in this case for Aspen (Aw)

y2bh = years until breast height age can be measured

SI_bh_Aw = Site index estimated with breast heigh age

'''

x_Aw=ComputeGypsySiteIndex(sp_Aw[0],  sp_Aw[1],  sp_Aw[2], sp_Aw[3])

bhage_Aw=x_Aw[0]
tage_Aw=x_Aw[1]
si_Aw=x_Aw[2]
y2bh_Aw= x_Aw[3]
SI_bh_Aw=x_Aw[4]

'''treeHeight is the Top Height or Htop in the paper'''
topHeight_Aw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Aw[0],  si_Aw,  tage_Aw)

print ' estimated Site Index for species Aw is:  ', si_Aw
print ' estimated Total age for species Aw is:  ', tage_Aw
print ' estimated BH age for species Aw is:  ', bhage_Aw
print ' estimated Site Index BH for species Aw is:  ',SI_bh_Aw
print ' estimated number of years until measuring BH becomes possible:  ',  y2bh_Aw


x_Sb=ComputeGypsySiteIndex(sp_Sb[0],  sp_Sb[1],  sp_Sb[2], sp_Sb[3])

bhage_Sb=x_Sb[0]
tage_Sb=x_Sb[1]
si_Sb=x_Sb[2]
y2bh_Sb= x_Sb[3]
SI_bh_Sb=x_Sb[4]

'''treeHeight is the Top Height or Htop in the paper'''
topHeight_Sb=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Sb[0],  si_Sb,  tage_Sb)

print ' estimated Site Index for species Sb is:  ', si_Sb
print ' estimated Total age for species Sb is:  ', tage_Sb
print ' estimated BH age for species Sb is:  ', bhage_Sb
print ' estimated Site Index BH for species Sb is:  ',SI_bh_Sb
print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Sb

x_Pl=ComputeGypsySiteIndex(sp_Pl[0],  sp_Pl[1],  sp_Pl[2], sp_Pl[3])

bhage_Pl=x_Pl[0]
tage_Pl=x_Pl[1]
si_Pl=x_Pl[2]
y2bh_Pl= x_Pl[3]
SI_bh_Pl=x_Pl[4]

'''treeHeight is the Top Height or Htop in the paper'''
topHeight_Pl=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Pl[0],  si_Pl,  tage_Pl)

print ' estimated Site Index for species Pl is:  ', si_Pl
print ' estimated Top Height for species Pl is:  ', topHeight_Pl
print ' estimated Total age for species Pl is:  ', tage_Pl
print ' estimated BH age for species Pl is:  ', bhage_Pl
print ' estimated Site Index BH for species Pl is:  ', SI_bh_Pl
print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Pl

x_Sw=ComputeGypsySiteIndex(sp_Sw[0],  sp_Sw[1],  sp_Sw[2], sp_Sw[3])

bhage_Sw=x_Sw[0]
tage_Sw=x_Sw[1]
si_Sw=x_Sw[2]
y2bh_Sw= x_Sw[3]
SI_bh_Sw=x_Sw[4]

'''treeHeight is the Top Height or Htop in the paper'''
topHeight_Sw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Sw[0],  si_Sw,  tage_Sw)

print ' estimated Site Index for species Sw is:  ', si_Sw
print ' estimated Top Height for species Sw is:  ', topHeight_Sw
print ' estimated Total age for species Sw is:  ', tage_Sw
print ' estimated BH age for species Sw is:  ', bhage_Sw
print ' estimated Site Index BH for species Sw is:  ', SI_bh_Sw
print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Sw

'''
si, bhage, and tage are passed on from the above. SDFs estimated iteratively
'''

'''I am using N from the original input sp_Aw etc as the input (N_Aw) etc 
I think it is suposed to be the density of the species at the bhage = 0, although 
the paper says current or inital density

'''

N_Aw = sp_Aw[4]
N_Sb = sp_Sb[4]
N_Sw = sp_Sw[4]
N_Pl = sp_Pl[4]




     
PS_Aw= sp_Aw[6]
PS_Sb= sp_Sb[6]
PS_Sw= sp_Sw[6]
PS_Pl= sp_Pl[6]


'''
percent stocking estimation is the first function of the Spatial approach and uses the same inputs described above plus

the PS which is the percent stocking measured in the field

one of the main purposes here is to estimate PSI, which is the Percent Stocking Index

'''
 


def PercentStockingModelSpatialAw (tage_Aw, SI_bh_Aw, PS_Aw):
    if SI_bh_Aw>0 and tage_Aw>0:
        b1      =       -14.9555 
        b2      =        0.45162 
        b3      =        1.59953 
        
        k2 = 1+ numpy.exp(b1 + (b2* ((numpy.log(tage_Aw +1))**2) )+ (b3* numpy.log(SI_bh_Aw)  )     )
        
        k1= 1+numpy.exp(b1 + (b2* ((numpy.log(50 +1))**2 )) + (b3* numpy.log(SI_bh_Aw))  )
        
        PSI_Aw = PS_Aw * k2/k1

        PS_Aw = PSI_Aw * k1/k2
        
    else:
        PSI_Aw = 0
        PS_Aw = 0
        
    return PSI_Aw, PS_Aw

PSM_Aw = PercentStockingModelSpatialAw (tage_Aw, SI_bh_Aw, PS_Aw)
PSI_Aw= PSM_Aw[0]
print PSI_Aw

 
 

def PercentStockingModelSpatialSb (tage_Sb, SI_bh_Sb, PS_Sb):
    if SI_bh_Sb>0 and tage_Sb>0:
        b1     =        -16.7154 
        b2     =        0.369843 
        b3     =        2.808537 
        k1= 1+ numpy.exp(b1 + (b2* ((numpy.log(50 +1))**2) )+ (b3* numpy.log(SI_bh_Sb) )   )
        
        k2= 1+ numpy.exp(b1 + (b2* (numpy.log(tage_Sb+1))**2) + (b3* numpy.log(SI_bh_Sb)   )    )
        
        PSI_Sb= PS_Sb *k2/k1
    else:
        PSI_Sb = 0
        
    return PSI_Sb

PSM_Sb = PercentStockingModelSpatialSb (tage_Sb, SI_bh_Sb, PS_Sb)
PSI_Sb= PSM_Sb
print PSI_Sb



def PercentStockingModelSpatialSw (tage_Sw, SI_bh_Sw, PS_Sw, PSI_Aw):
    if SI_bh_Sw>0 and tage_Sw>0:     
        b1      =       -21.8721 
        b2      =       0.395767 
        b3      =       4.128582 
        if PSI_Aw==0:
            x1=0
        if PSI_Aw>0:
            x1=1
        k2 = 1+ numpy.exp(b1 + (b2* ((numpy.log(tage_Sw+1))**2) ) + (b3* numpy.log(SI_bh_Sw)) + (x1*(PSI_Aw/b3)/50) )
        k1 = 1+ numpy.exp(b1 + (b2* ((numpy.log(50 +1))**2) ) + (b3* numpy.log(SI_bh_Sw) ) + (x1*(PSI_Aw/b3)/50 )   )
        PSI_Sw = PS_Sw *k2/k1
    else:
        PSI_Sw = 0
        
    return PSI_Sw
    
PSM_Sw = PercentStockingModelSpatialSw (tage_Sw, SI_bh_Sw, PS_Sw, PSI_Aw)
PSI_Sw= PSM_Sw
print PSI_Sw


    
def PercentStockingModelSpatialSw (tage_Pl, SI_bh_Pl, PS_Pl, PSI_Aw, PSI_Sb, PSI_Sw):
    if SI_bh_Pl>0 and tage_Pl>0:   
        b1     =       -12.2731  
        b2     =        0.23981  
        b3     =        2.17610  
        b4     =        0.02492  
        b5     =        0.08990  
        b6     =        0.17058  
        if PSI_Aw==0:
            x1=0
        if PSI_Aw>0:
            x1=1
        if PSI_Sb==0:
            x2=0
        if PSI_Sb>0:
            x2=1
        if PSI_Sw==0:
            x3=0
        if PSI_Sw>0:
            x3=1
            
        k1= 1+ numpy.exp(b1 + (b2* (numpy.log(50 +1))**2) + (b3* numpy.log(SI_bh_Pl))  )
        
        k2 = 1+ numpy.exp(b1 + (b2* (numpy.log(tage_Pl+1))**2) + (b3* (numpy.log(SI_bh_Pl)) ) )
       
        M = (b4*x1*PSI_Aw) + (b5*x2*((PSI_Sb)**0.5)) + (b6*x3*((PSI_Sw)**0.5)  )
       
        PSI_Pl= PS_Pl* (k2+M)/(k1+M)
        PS_Pl = PSI_Pl * (k1+M)/(k2+M)
    else:
        PSI_Pl = 0
        PS_Pl = 0
        
    return PSI_Pl
    
PSM_Pl = PercentStockingModelSpatialSw (tage_Pl, SI_bh_Pl, PS_Pl, PSI_Aw, PSI_Sb, PSI_Sw)
PSI_Pl= PSM_Pl
print PSI_Pl
     
     
'''
this estimation of density using the Spatial approach is very similar to the Non-Spatial approach except that it uses  PSI estimated above

in addition to the SDFs

'''


def DensityModelSpatialAw (N_Aw, PSI_Aw, bhage_Aw, SI_bh_Aw):
    if N_Aw>0  and bhage_Aw>0 and SI_bh_Aw>0 :
        c0      =       0.71123 
        c1      =       7.015511
        SDF_Aw0=1000
        SDF_Aw1=0
        while abs(SDF_Aw0-SDF_Aw1)>0.00000001:
            b1 =-((1/numpy.sqrt(SDF_Aw0/1000))+ numpy.sqrt(1+ (50/((SDF_Aw0**0.5)*numpy.log(1+50)) ) ) + (c0* numpy.log(1+ (PSI_Aw/(SDF_Aw0**0.5)) )/c1 ) ) * numpy.log(1+50)
            b2=(c0/4)*((SDF_Aw0**0.5)**(1/SDF_Aw0))
            
            k =  (c1 + numpy.log(SDF_Aw0)+ (numpy.log(1+PSI_Aw)/SDF_Aw0))/SDF_Aw0 
            
            b3=(1+c0)*(SDF_Aw0**k)
            
            k1 = 1+ numpy.exp(b1 +(b2* SI_bh_Aw)+ (b3* numpy.log(50 +1))  )    
            k2 = 1+ numpy.exp(b1 +(b2 * SI_bh_Aw) + (b3* numpy.log(bhage_Aw +1))  )
            SDF_Aw1= N_Aw * (k2/k1)
            SDF_Aw0=(SDF_Aw0+SDF_Aw1)/2
        SDF_Sp_Aw = SDF_Aw1
        N_bhage_Sp_Aw_0 = SDF_Sp_Aw * (1+ numpy.exp(b1 +(b2* SI_bh_Aw)+ (b3* numpy.log(50+1) ))) / (1+ numpy.exp(b1 + (b2* SI_bh_Aw )+ (b3* numpy.log(1+0) )) )
        #it is zero because here bhage is zero
        N_bhage_Sp_Aw = SDF_Sp_Aw *k1/k2
    else:
        N_bhage_Sp_Aw = 0
        SDF_Sp_Aw = 0
        N_bhage_Sp_Aw_0 = 0
        
    return N_bhage_Sp_Aw_0, SDF_Sp_Aw, N_bhage_Sp_Aw

N_Sp_Aw = DensityModelSpatialAw (N_Aw, PSI_Aw, bhage_Aw, SI_bh_Aw)
SDF_Sp_Aw = N_Sp_Aw[1]
N_bhage_Sp_Aw_0 = N_Sp_Aw [0]
N_bhage_Sp_Aw = N_Sp_Aw[2]
print N_Sp_Aw



def DensityModelSpatialSb (N_Sb, PSI_Sb, tage_Sb, SI_bh_Sb):
    if N_Sb>0  and bhage_Sb>0 and SI_bh_Sb>0:
        c1    =         -25.7666 
        c2    =         0.192351 
        c3    =         2.718748 
        SDF_Sb0=1000
        SDF_Sb1=0
        while abs(SDF_Sb0-SDF_Sb1)>0.00000001:
            b1=(c1/((numpy.sqrt(SDF_Sb0/1000)+numpy.log(1+ 50) )**c2) ) - (numpy.log(1+PSI_Sb)/(1+c3) )
            b2=c3;
            b3=c3* (SDF_Sb0**(1/SDF_Sb0) )
            
            k1=1+ numpy.exp(b1 +(b2* numpy.log(SI_bh_Sb))+ (b3* numpy.log(50 +1)) )
            k2 = 1+ numpy.exp (b1 +(b2* numpy.log( SI_bh_Sb))+ (b3* numpy.log(tage_Sb+1)) )
            SDF_Sb1= N_Sb * (k2/k1)
            SDF_Sb0=(SDF_Sb0+SDF_Sb1)/2
        SDF_Sp_Sb = SDF_Sb1
        #it is zero because age, here tage is zero
        N_tage_Sp_Sb_0 = SDF_Sp_Sb * (1+ numpy.exp(b1 +(b2*numpy.log( SI_bh_Sb ) )+ (b3* numpy.log(50+1) ))) / (1+ numpy.exp(b1 + (b2*numpy.log( SI_bh_Sb ) )+ (b3* numpy.log(1 + 0) )) )
        N_tage_Sp_Sb = SDF_Sp_Sb *k1/k2
    else:
        N_tage_Sp_Sb = 0
        SDF_Sp_Sb = 0
        N_tage_Sp_Sb_0 = 0
        
    return N_tage_Sp_Sb_0, SDF_Sp_Sb, N_tage_Sp_Sb
            
N_Sp_Sb = DensityModelSpatialSb (N_Sb, PSI_Sb, tage_Sb, SI_bh_Sb)

N_tage_Sp_Sb_0 = N_Sp_Sb[0]     
SDF_Sp_Sb = N_Sp_Sb[1]
N_tage_Sp_Sb = N_Sp_Sb[2]
print N_Sp_Sb
        


def DensityModelSpatialSw (N_Sw, PSI_Sw, tage_Sw, SI_bh_Sw, SDF_Sp_Aw):
    if N_Sw>0  and bhage_Sw>0 and SI_bh_Sw>0:
        c1       =      -254.391  
        c2       =      1.146709  
        c3       =      2.202149
        if SDF_Sp_Aw==0:
            z1=0
        if SDF_Sp_Aw>0:
            z1=1
        SDF_Sw0=1000
        SDF_Sw1=0
        while abs(SDF_Sw0-SDF_Sw1)>0.00000001:
            b1=(c1/( (numpy.log(SDF_Sw0)+numpy.log(1+50) )**c2)) +  (z1*((1+SDF_Sp_Aw/1000)**0.5))+(numpy.log(1+SDF_Sw0)/10)
            b2=c3
            b3=c3*(SDF_Sw0**(1/SDF_Sw0))*((numpy.sqrt(1+PSI_Sw))**(-1/10))
            k1=1+ numpy.exp (b1 +(b2*numpy.log( SI_bh_Sw ))+ (b3* numpy.log(50 + 1)) )
            k2=1+ numpy.exp ( b1 + (b2*numpy.log( SI_bh_Sw ))+ (b3* numpy.log(tage_Sw  +1))  )
            SDF_Sw1= N_Sw * (k2/k1)
            SDF_Sw0=(SDF_Sw0+SDF_Sw1)/2
        SDF_Sp_Sw = SDF_Sw1
        N_tage_Sp_Sw_0 = SDF_Sp_Sw * (1+ numpy.exp(b1 + (b2*numpy.log( SI_bh_Sw ) )+ (b3* numpy.log(50+1) ))) / (1+ numpy.exp(b1 + (b2*numpy.log( SI_bh_Sw) )+ (b3* numpy.log(1 + 0) )) )
        N_tage_Sp_Sw = SDF_Sp_Sw *k1/k2
    else:
        N_tage_Sp_Sw = 0
        SDF_Sp_Sw = 0
        N_tage_Sp_Sw_0 = 0        
        
    return N_tage_Sp_Sw_0, SDF_Sp_Sw, N_tage_Sp_Sw


            
N_Sp_Sw =  DensityModelSpatialSw (N_Sw, PSI_Sw, tage_Sw, SI_bh_Sw, SDF_Sp_Aw)          
            
N_tage_Sp_Sw_0 = N_Sp_Sw[0]     
SDF_Sp_Sw = N_Sp_Sw[1]  
N_tage_Sp_Sw = N_Sp_Sw[2]         

print N_Sp_Sw
            
            
            
def DensityModelSpatialPl (N_Pl, PSI_Pl, tage_Pl, SI_bh_Pl, SDF_Sp_Aw, SDF_Sp_Sb, SDF_Sp_Sw):
    if N_Pl>0  and bhage_Pl>0 and SI_bh_Pl>0:
        c1       =      -3.09711
        c2       =      -512.394
        c3       =       1.14981
        c4       =      1.027108
        c5       =      -0.05479
        c6       =       4.12191
        if SDF_Sp_Aw==0:
            z1=0
        if SDF_Sp_Aw>0:
            z1=1
        if SDF_Sp_Sw==0:
            z2=0
        if SDF_Sp_Sw>0:
            z2=1
        if SDF_Sp_Sb==0:
            z3=0
        if SDF_Sp_Sb>0:
            z3=1
        SDF_Pl0=1000
        SDF_Pl1=0
        while abs(SDF_Pl0-SDF_Pl1)>0.00000001:
            m=(c2/((numpy.sqrt(SDF_Pl0))**c3)) - (numpy.log(1+PSI_Pl)/(1 +c4) )
            
            b1=( c1+(z1*(SDF_Sp_Aw/1000)/2 )+ (z2*(SDF_Sp_Sw/1000)/3)  + (z3*(SDF_Sp_Sb/1000)/4 ) ) + m
            
            
            b2=c4/(((SDF_Pl0)**0.5)**c5)
            
            k= (1+  (c6*((SDF_Pl0)**0.5) ))/SDF_Pl0
            
            b3=c4*(SDF_Pl0**k)
            
            k1 = 1+ numpy.exp(b1 + (b2* numpy.log(SI_bh_Pl ))+ (b3* numpy.log(50 + 1)) )
            k2 = 1+ numpy.exp(b1 + (b2* numpy.log(SI_bh_Pl ))+ ( b3* numpy.log(tage_Pl +1)) )
            SDF_Pl1= N_Pl * (k2/k1)
            SDF_Pl0=(SDF_Pl0+SDF_Pl1)/2
        SDF_Sp_Pl = SDF_Pl1
        N_tage_Sp_Pl_0 = SDF_Sp_Pl * (1+ numpy.exp(b1 + (b2*numpy.log( SI_bh_Pl ) )+ (b3* numpy.log(50+1) ))) / (1+ numpy.exp(b1 + (b2*numpy.log( SI_bh_Pl) )+ (b3* numpy.log(1 + 0) )) )
        N_tage_Sp_Pl = SDF_Sp_Pl *k1/k2
        
    else:
        N_tage_Sp_Pl = 0
        SDF_Sp_Pl = 0
        N_tage_Sp_Pl_0 = 0        
        
    return N_tage_Sp_Pl_0, SDF_Sp_Pl, N_tage_Sp_Pl
            
N_Sp_Pl =  DensityModelSpatialPl (N_Pl, PSI_Pl, tage_Pl, SI_bh_Pl, SDF_Sp_Aw, SDF_Sp_Sb, SDF_Sp_Sw)

N_tage_Sp_Pl_0 = N_Sp_Pl[0]     
SDF_Sp_Pl = N_Sp_Pl[1]  
N_tage_Sp_Pl = N_Sp_Pl[2]          

print N_Sp_Pl
        

total_Sp_N=(N_bhage_Sp_Aw + N_tage_Sp_Pl + N_tage_Sp_Sw + N_tage_Sp_Sb)
SC_Sp_Aw = N_bhage_Sp_Aw/total_Sp_N
SC_Sp_Sw = N_tage_Sp_Sw/total_Sp_N
SC_Sp_Sb = N_tage_Sp_Sb/total_Sp_N
SC_Sp_Pl = N_tage_Sp_Pl/total_Sp_N



'''
here too, the basal area increment is similar to the non-spatial version except that it also uses PSI in addition to SDFs

'''


def BasalAreaIncrementSpatialAw (bhage_Aw, N_bhage_Sp_Aw_0, SI_bh_Aw, N_bhage_Sp_Aw , SC_Sp_Aw, PSI_Aw, BA_Aw):
    if bhage_Aw>=0:
        a1        =     0.055906 
        a2        =     0.054216 
        a3        =     1.240035 
        a4        =     -0.05515 
        a5        =     0.218326 
        a6        =     0.749594 
        k1 = (10**-4)*a1*(bhage_Aw**2)*numpy.exp(-a2*bhage_Aw) * (SC_Sp_Aw**a5) *((numpy.log (1+(N_bhage_Sp_Aw_0* numpy.sqrt(1+bhage_Aw) ))) **2) *SI_bh_Aw * (PSI_Aw**a6)
        k2 = ((1+BA_Aw)**a3) * (1+ numpy.exp(1 - (numpy.log(1+(SC_Sp_Aw**2) )/2 )   ))
        k = a4 * numpy.log(0.01+(bhage_Aw/10)) 
        BAinc_SP_Aw = (k1/k2)+k
    else:
        BAinc_SP_Aw = 0
    return BAinc_SP_Aw
BAinc_Sp_Aw =  BasalAreaIncrementSpatialAw (bhage_Aw, N_bhage_Sp_Aw_0, SI_bh_Aw, N_bhage_Sp_Aw , SC_Sp_Aw, PSI_Aw, BA_Aw)
            
print BAinc_Sp_Aw



def BasalAreaIncrementSpatialSb (bhage_Sb, N_tage_Sp_Sb_0, SI_bh_Sb, SC_Sp_Sb, PSI_Sb, BA_Sb):
    if bhage_Sb>=0:
        a1      =       0.333889 
        a2      =       0.047669 
        a3      =        0.03635 
        a4      =       0.484915 
           
        k1 = (10**-4)* a1 * numpy.exp(-a2 * bhage_Sb) * bhage_Sb**((a1**0.5)+a2 ) * (SC_Sp_Sb**a3) 
        
        k = (1+(N_tage_Sp_Sb_0**0.5) * ((1+bhage_Sb)**0.5) ) * numpy.log(1+SI_bh_Sb) * numpy.exp(-(N_tage_Sp_Sb_0/4)/10000) * PSI_Sb**a4/ ((1+BA_Sb )**a2)
        
        BAinc_Sp_Sb=k*k1
    else:
        BAinc_SP_Sb = 0
        
    return BAinc_Sp_Sb

print BasalAreaIncrementSpatialSb (bhage_Sb, N_tage_Sp_Sb_0, SI_bh_Sb, SC_Sp_Sb, PSI_Sb, BA_Sb)



def BasalAreaIncrementSpatialSw (bhage_Sw, N_tage_Sp_Sw_0, SI_bh_Sw,  SC_Sp_Sw, PSI_Sw, BA_Sw):
    if bhage_Sw>=0:
        a1     =        0.041072
        a2     =        0.067012
        a3     =        -0.00163
        a4     =        5.701986
        a5     =        2.222453
        a6     =        0.001126
        a7     =        0.368267
        if SDF_Sp_Aw==0:
            z1=0
        if SDF_Sp_Aw>0:
            z1=1
        if SDF_Sp_Pl==0:
            z2=0
        if SDF_Sp_Pl>0:
            z2=1
        if SDF_Sp_Sb==0:
            z3=0
        if SDF_Sp_Sb>0:
            z3=1
            
        k=(a4* z1* numpy.log(1+(SDF_Sp_Aw/10000) )) + (a5*z2* numpy.log(1+(SDF_Sp_Pl/10000) ) )+ (z3* numpy.log(1+(SDF_Sp_Sb/10000) ))
        
        k1 = (10**-4)* a1* ((a2+bhage_Sw)**2) * ( (1+bhage_Sw)**((a1**0.5)+a2-a3) )* numpy.exp(-a2*bhage_Sw)*  (SC_Sp_Sw**a6) * (PSI_Sw**a7)
        
        k2 = 1+ numpy.exp(1+ k +(numpy.log(1+((N_tage_Sp_Sw_0**0.5)/10000)) /2 ) + (a3*numpy.log(1+BA_Sw )) ) 
        
        m =  ( (numpy.log (1+(N_tage_Sp_Sw_0 * numpy.sqrt(1+bhage_Sw) )))**2  ) * (SI_bh_Sw ** 0.5) * numpy.exp(-(N_tage_Sp_Sw_0/10)/10000)
        
        BAinc_Sp_Sw = k1*m / k2
    else:
        BAinc_SP_Sw = 0
        
    return BAinc_Sp_Sw
    
print BasalAreaIncrementSpatialSw (bhage_Sw, N_tage_Sp_Sw_0, SI_bh_Sw, SC_Sp_Sw, PSI_Sw, BA_Sw)



def BasalAreaIncrementSpatialPl (bhage_Pl, N_tage_Sp_Pl_0, SI_bh_Pl,  SC_Sp_Pl, PSI_Pl, BA_Pl):
    if bhage_Pl>=0:
        a1        =     0.067391 
        a2        =     0.054113 
        a3        =     0.213767 
        a4        =     0.977498 
        a5        =     -0.00452 
        a6        =     1.080421 
        if SDF_Sp_Aw==0:
            z1=0
        if SDF_Sp_Aw>0:
            z1=1
        if SDF_Sp_Sw==0:
            z2=0
        if SDF_Sp_Sw>0:
            z2=1
        if SDF_Sp_Sb==0:
            z3=0
        if SDF_Sp_Sb>0:
            z3=1
        
        k=z1* numpy.log (1+(SDF_Sp_Aw/1000) ) + (z2 * numpy.log(1+(SDF_Sp_Sw/1000 ))/2 ) + (z3* numpy.log (1+(SDF_Sp_Sb/1000) )/2 )
        
        k1 =(10**-4)* a1* bhage_Pl * numpy.exp(-a2*bhage_Pl) * ( 1 + numpy.log(1+bhage_Pl)/2 ) *PSI_Pl
        
        k2 =  1+ numpy.exp( (k/2)+ numpy.log(1+((N_tage_Sp_Pl_0/3)/10000) )  - (a3*(SC_Sp_Pl**0.5)) + (a4* numpy.log(1+BA_Pl)) ) 
        
        m1 = (1+a3+ (SI_bh_Pl**a6) ) * (N_tage_Sp_Pl_0**0.5) * numpy.exp(-(N_tage_Sp_Pl_0/3)/10000)
        
        m2 = a5* numpy.log(0.01 + (bhage_Pl/10))
        
        BAinc_Sp_Pl = (k1*m1/k2)+m2
    else:
        BAinc_SP_Sb = 0
        
    return BAinc_Sp_Pl

print BasalAreaIncrementSpatialPl (bhage_Pl, N_tage_Sp_Pl_0, SI_bh_Pl,  SC_Sp_Pl, PSI_Pl, BA_Pl)


'''
Gross total volume is estimated only using species specific Basal Area and Tp height

'''

        
def GrossTotalVolume(sp_Aw, sp_Sb, sp_Sw, sp_Pl, BA_Aw, BA_Sb, BA_Sw, BA_Pl, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl):
    if topHeight_Aw > 1.3:
        if sp_Aw[0] == 'Aw' or \
           sp_Aw[0] == 'Bw' or \
           sp_Aw[0] == 'Pb' or \
           sp_Aw[0] == 'A' or \
           sp_Aw[0] == 'H':
              a1     =        0.248718 
              a2     =         0.98568 
              a3     =        0.857278 
              a4     =        -24.9961
              Tvol_Aw = a1* (BA_Aw**a2) * (topHeight_Aw**a3) * numpy.exp(1+(a4/( (topHeight_Aw**2)+1)) )
    elif topHeight_Aw < 1.3:
        Tvol_Aw = 0
        
              
    if topHeight_Sb > 1.3:
        if sp_Sb[0] == 'Sb' or \
           sp_Sb[0] == 'Lt' or \
           sp_Sb[0] == 'La' or \
           sp_Sb[0] == 'Lw' or \
           sp_Sb[0] == 'L':
               b1    =          0.48628 
               b2    =         0.982962 
               b3    =         0.910603
               Tvol_Sb = b1 * BA_Sb**b2 * topHeight_Sb**b3
    elif topHeight_Sb < 1.3:
        Tvol_Sb = 0
               
    if topHeight_Sw > 1.3:
        if sp_Sw[0] == 'Sw' or \
           sp_Sw[0] == 'Se' or \
           sp_Sw[0] == 'Fd' or \
           sp_Sw[0] == 'Fb' or \
           sp_Sw[0] == 'Fa':
               b1    =          0.41104 
               b2    =         0.983108 
               b3    =         0.971061
               Tvol_Sw = b1 * BA_Sw**b2 * topHeight_Sw**b3
    elif topHeight_Sw < 1.3:
        Tvol_Sw = 0
               
    if topHeight_Pl > 1.3:
        if sp_Pl[0] == 'P' or \
           sp_Pl[0] == 'Pl' or \
           sp_Pl[0] == 'Pj' or \
           sp_Pl[0] == 'Pa' or \
           sp_Pl[0] == 'Pf':
               a1     =        0.194086 
               a2     =        0.988276 
               a3     =        0.949346 
               a4     =        -3.39036
               Tvol_Pl = a1* (BA_Pl**a2) * (topHeight_Pl **a3) * numpy.exp(1+(a4/( (topHeight_Pl**2)+1)) )
    elif topHeight_Pl < 1.3:
        Tvol_Pl = 0
               
    return Tvol_Aw, Tvol_Sb, Tvol_Sw, Tvol_Pl
    
Tvol = GrossTotalVolume(sp_Aw, sp_Sb, sp_Sw, sp_Pl, BA_Aw, BA_Sb, BA_Sw, BA_Pl, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl)

Tvol_Aw = Tvol[0]
Tvol_Sb = Tvol[1]
Tvol_Sw = Tvol[2]
Tvol_Pl = Tvol[3]

print Tvol_Aw, Tvol_Sb, Tvol_Sw, Tvol_Pl


'''

Merchantable volume only new variables are the stump diameter outside bark, stump height and top diameter inside bark

'''

# to declare variable as double k_Sb= np.asarray(k_Sb, type = np.float64)

'''
I used this if here to avoid division by zero when density is zero, i.e., when the species is absent in the plot.

'''

if N_Aw >0:
    k_Aw = (BA_Aw * 10000 / N_Aw)**0.5
else:
    k_Aw = 0
    
if N_Sb >0:
    k_Sb=(BA_Sb * 10000 / N_Sb)**0.5
else:
    k_Sb = 0

if N_Sw >0:
    k_Sw=(BA_Sw * 10000 / N_Sw)**0.5
else: 
    k_Sw= 0
    
if N_Pl > 0:
    k_Pl=(BA_Pl * 10000 / N_Pl)**0.5
else:
    k_Pl= 0

StumpDOB_Aw=sp_Aw[7]
StumpHeight_Aw =sp_Aw[8]
TopDib_Aw = sp_Aw[9]

StumpDOB_Sb=sp_Sb[7]
StumpHeight_Sb =sp_Sb[8]
TopDib_Sb = sp_Sb[9]

StumpDOB_Sw=sp_Sw[7]
StumpHeight_Sw =sp_Sw[8]
TopDib_Sw = sp_Sw[9]

StumpDOB_Pl=sp_Pl[7]
StumpHeight_Pl =sp_Pl[8]
TopDib_Pl = sp_Pl[9]



def MerchantableVolumeAw(k_Aw, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw):
    if k_Aw > 0 and  topHeight_Aw>0:
        b0    =         0.993673 
        b1    =         923.5825 
        b2    =         -3.96171 
        b3    =         3.366144 
        b4    =         0.316236 
        b5    =         0.968953 
        b6    =         -1.61247
        k1 = Tvol_Aw * k_Aw**b0
        k2 =(b1* (topHeight_Aw**b2) * (StumpDOB_Aw**b3) * (StumpHeight_Aw**b4) * (TopDib_Aw**b5)  * (k_Aw**b6) ) +k_Aw
        MVol_Aw=k1/k2
    else:
        MVol_Aw=0
             
    return MVol_Aw
    

    
MVol_Aw = MerchantableVolumeAw(k_Aw, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw)   
   
   

def MerchantableVolumeSb(k_Aw, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb):    
    if k_Sb > 0 and  topHeight_Sb>0:
        if sp_Sb[0] == 'Sb' or \
           sp_Sb[0] == 'Lt' or \
           sp_Sb[0] == 'La' or \
           sp_Sb[0] == 'Lw' or \
           sp_Sb[0] == 'L':
               b0     =         0.98152
               b1     =        0.678011
               b2     =        -1.10256
               b3     =        4.148139
               b4     =        0.511391
               b5     =        1.484988
               b6     =        -3.26425
               StumpDOB=sp_Sb[7]
               StumpHeight =sp_Sb[8]
               TopDib = sp_Sb[9]
               MVol_Sb = (Tvol_Sb * k_Sb**b0) / (b1* (topHeight_Sb**b2) * (StumpDOB**b3) * (StumpHeight**b4) * (TopDib**b5) * (k_Sb**b6) +k_Sb)
    else:
        MVol_Sb=0
        
    return MVol_Sb               
               
MVol_Sb = MerchantableVolumeSb(k_Aw, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb) 



def MerchantableVolumeSw(k_Sw, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw):               
    if k_Sw > 0 and  topHeight_Sw>0:
        if sp_Sw[0] == 'Sw' or \
           sp_Sw[0] == 'Se' or \
           sp_Sw[0] == 'Fd' or \
           sp_Sw[0] == 'Fb' or \
           sp_Sw[0] == 'Fa':
               b0     =        0.996262
               b1     =        7.021736
               b2     =        -1.77615
               b3     =         1.91562
               b4     =          0.4111
               b5     =        1.024803
               b6     =        -0.80121
               MVol_Sw = (Tvol_Sw * k_Sw**b0) / (b1* (topHeight_Sw**b2) * (sp_Sw[7]**b3) * (sp_Sw[8]**b4) * (sp_Sw[9]**b5) * (k_Sw**b6) +k_Sw)
    else:
        MVol_Sw=0               
               
    return MVol_Sw

MVol_Sw = MerchantableVolumeSw(k_Sw, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw)



def MerchantableVolumePl (k_Pl, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl):           
    if k_Pl > 0 and  topHeight_Pl>0:
        if sp_Pl[0] == 'P' or \
           sp_Pl[0] == 'Pl' or \
           sp_Pl[0] == 'Pj' or \
           sp_Pl[0] == 'Pa' or \
           sp_Pl[0] == 'Pf':
               b0   =          0.989889
               b1   =          1.055091
               b2   =          -0.19072
               b3   =          4.915593
               b4   =           0.42574
               b5   =          1.006379
               b6   =          -4.87808
               MVol_Pl = (Tvol_Pl * k_Pl**b0) / (b1* (topHeight_Pl**b2) * (sp_Pl[7]**b3) * (sp_Pl[8]**b4) * (sp_Pl[9]**b5) * (k_Pl**b6) +k_Pl)
    else:
        MVol_Pl=0
               
    return MVol_Pl
     
MVol_Pl = MerchantableVolumePl(k_Pl, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl)


print MVol_Aw, MVol_Sb, MVol_Sw, MVol_Pl




   

