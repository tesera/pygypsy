# -*- coding: utf-8 -*-
""" Functions 
Created on Wed Apr  6 08:20:38 2016

@author: juliannosambatti
"""

import numpy
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge

from scipy.optimize import fmin


"""
estimating Sit, total age, and bhage using asaCompileAgeGivenSpSiHt functions
"""
# input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Pl=['Pl', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sw=['Sw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

'''
b_hage = Breast Height Age
tage = Total age

the algorithm accepts either one

si_Aw  =  estimated Site intex according to the paper in this case for Aspen (Aw)

y2bh = years until breast height age can be measured

SI_bh_Aw = Site index estimated with breast heigh age

'''



  
'''
N_bh_Aw = estimated N and should be equal N_Aw (for Aspen in this case Aw)

The main purpose of this step is to estimate SDF that is employed in other formulas

'''


def densityNonSpatialAw (sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings = True):
    N_est_Aw = 0
    SDF_Aw0 = 0
    if N_Aw  <= 0: return N_est_Aw, SDF_Aw0            
    if bhage_Aw <= 0 or SI_bh_Aw <= 0: return N_est_Aw, SDF_Aw0
    if sp_Aw[0] == 'Aw' or \
       sp_Aw[0] == 'Bw' or \
       sp_Aw[0] == 'Pb' or \
       sp_Aw[0] == 'A' or \
       sp_Aw[0] == 'H':
           c0=0.717966
           c1=6.67468
           
           SDF_Aw0 = N_Aw # best SDF_Aw guess
           acceptableDiff= 0.00001
           NDiffFlag = False
           iterCount = 0 
           while NDiffFlag == False:
               
               b3=(1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)
               b2=(c0/4) * (SDF_Aw0**0.5)**(1/(SDF_Aw0))
               
               b1= -( (1/((SDF_Aw0/1000)**(0.5)) ) + numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1)))) ) * numpy.log(50+1)
             
               
               k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
               k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(1+bhage_Aw)))
               
               N_est_Aw = SDF_Aw0*k1/k2
               
               
               if abs(N_Aw-N_est_Aw) < acceptableDiff:
                   NDiffFlag = True
               
               else: 
                   N_est_Aw = (N_Aw + N_est_Aw)/2
                   SDF_Aw0 = N_est_Aw *k2/k1
                   #print 'Aw',  N_est_Aw, SDF_Aw0
                                      
               iterCount = iterCount + 1
               if iterCount == 150 and printWarnings == True:
                   print '\n GYPSYNonSpatial.densityNonSpatialAw()'
                   print ' Slow convergence'
                   return N_est_Aw, SDF_Aw0
 
                   
    return N_est_Aw, SDF_Aw0


 
      
def densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb, printWarnings = True):
    N_est_Sb = 0
    SDF_Sb0 = 0          
    if N_Sb>0:
        if tage_Sb > 0 or SI_bh_Sb > 0:
            if sp_Sb[0] == 'Sb' or \
               sp_Sb[0] == 'Lt' or \
               sp_Sb[0] == 'La' or \
               sp_Sb[0] == 'Lw' or \
               sp_Sb[0] == 'L':
                   c1=-26.3836
                   c2=0.166483
                   c3=2.738569
                   
                   SDF_Sb0 = N_Sb # best SDF_Sb guess
                   acceptableDiff= 0.00001
                   NDiffFlag = False
                   iterCount = 0 
                   
                   while abs(N_Sb-N_est_Sb) > acceptableDiff:
                       b2=c3
                       b3=c3*(SDF_Sb0**(1/SDF_Sb0))
                       
                       b1=c1/ ((((SDF_Sb0/1000)**0.5)+numpy.log(50+1))**c2)
                       
                       k1=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+50)))
                       k2=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+tage_Sb)))
                      
                       N_est_Sb = SDF_Sb0*k1/k2
                            
                       if abs(N_Sb-N_est_Sb) < acceptableDiff:
                           NDiffFlag = True
                       
                       else: 
                           N_est_Sb = (N_Sb + N_est_Sb)/2
                           SDF_Sb0 = N_est_Sb * k2/k1
                           #print 'Sb', N_est_Sb, SDF_Sb0
                                              
                       iterCount = iterCount + 1
                       if iterCount == 150 and printWarnings == True:
                           print '\n GYPSYNonSpatial.densityNonSpatialSb()'
                           print ' Slow convergence'
                           return N_est_Sb, SDF_Sb0
                           
                   
                  
                   
    return N_est_Sb, SDF_Sb0
    

     

              
def densityNonSpatialSw(sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw0, N_Sw, printWarnings = True):
    N_est_Sw = 0
    SDF_Sw0 = 0         
    if N_Sw>0:
        if tage_Sw > 0 or SI_bh_Sw > 0:
            if sp_Sw[0] == 'Sw' or \
               sp_Sw[0] == 'Se' or \
               sp_Sw[0] == 'Fd' or \
               sp_Sw[0] == 'Fb' or \
               sp_Sw[0] == 'Fa':
                   if SDF_Aw0==0:
                       z1=0
                   elif SDF_Aw0>0:
                       z1=1
                   c1=-231.617
                   c2=1.176995
                   c3=1.733601
                   
                   SDF_Sw0 = N_Sw # best SDF_Sb guess
                   acceptableDiff= 0.00001
                   NDiffFlag = False
                   iterCount = 0 
                   while abs(N_Sw-N_est_Sw)> acceptableDiff:
                       
                       b3=c3*(SDF_Sw0**(1/SDF_Sw0))
                       b2=c3
                       b1=(c1/((numpy.log(SDF_Sw0)+numpy.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000))**0.5))
                       k1=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(50+1)))
                       k2=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(1+tage_Sw)))
                       
                       N_bh_Sw=SDF_Sw0*k1/k2
                       
                       if abs(N_Sw-N_est_Sw) < acceptableDiff:
                           NDiffFlag = True
                       else: 
                           N_est_Sw = (N_Sw + N_est_Sw)/2
                           SDF_Sw0 = N_est_Sw * k2/k1
                           #print 'Sw', N_est_Sw, SDF_Sw0
                           
                       iterCount = iterCount + 1
                       if iterCount == 150 and printWarnings == True:
                           print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                           print ' Slow convergence'
                           return N_est_Sw, SDF_Sw0
                       
                       
                    
              
    return N_est_Sw, SDF_Sw0


 

                
def densityNonSpatialPl(sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, N_Pl, printWarnings = True):
    N_est_Pl = 0
    SDF_Pl0 = 0  
    if N_Pl>0:
        if tage_Pl > 0 or SI_bh_Pl > 0:               
            if sp_Pl[0] == 'P' or \
               sp_Pl[0] == 'Pl' or \
               sp_Pl[0] == 'Pj' or \
               sp_Pl[0] == 'Pa' or \
               sp_Pl[0] == 'Pf':
                   c1=-5.25144
                   c2=-483.195
                   c3=1.138167
                   c4=1.017479
                   c5=-0.05471
                   c6=4.11215
                   if SDF_Aw0==0:
                       z1=0
                   elif SDF_Aw0>0:
                       z1=1
                   if SDF_Sw0==0:
                       z2=0
                   elif SDF_Sw0>0:
                       z2=1
                   if SDF_Sb0==0:
                       z3=0
                   elif SDF_Sb0>0:
                       z3=1
                       
                   SDF_Pl0 = N_Pl # best SDF_Sb guess
                   acceptableDiff= 0.00001
                   NDiffFlag = False
                   iterCount = 0
                   while abs(N_Pl-N_est_Pl)>acceptableDiff:
                       k=(1+(c6*(SDF_Pl0**0.5)))/SDF_Pl0    
                       b3=c4*(SDF_Pl0**k)
                       b2=c4/((SDF_Pl0**0.5)**c5)
                       
                       b1=(c1+(z1*(SDF_Aw0/1000)/2)+(z2*(SDF_Sw0/1000)/3)+(z3*(SDF_Sb0/1000)/4))+(c2/((SDF_Pl0**0.5)**c3))
                       
                       k1=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Pl))+(b3*numpy.log(50+1)))
                       k2=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Pl))+(b3*numpy.log(1+tage_Pl)))
                
                       N_est_Pl=SDF_Pl0*k1/k2
                       
                       if abs(N_Pl-N_est_Pl) < acceptableDiff:
                           NDiffFlag = True
                       else: 
                           N_est_Pl = (N_Pl + N_est_Pl)/2
                           SDF_Pl0 = N_est_Pl * k2/k1
                           #print 'Pl', N_est_Pl, SDF_Pl0
                           
                       iterCount = iterCount + 1
                       if iterCount == 150 and printWarnings == True:
                           print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                           print ' Slow convergence'
                           return N_est_Pl, SDF_Pl0
            
                   
    return N_est_Pl, SDF_Pl0
    
    
'''The purpose of the functiona below is to etimate N given that SDF have been estimated '''

def minimumN_SDF_Aw (SDF_Aw0, bhage_Aw, SI_bh_Aw):
    x0 = [200.0]
    optimize = fmin (densityAw, x0 , args = (bhage_Aw, SI_bh_Aw))
    
    return optimize




def densityAw (SDF_Aw0, bhage_Aw, SI_bh_Aw):
    
    if SDF_Aw0 > 0:
        c0=0.717966
        c1=6.67468
        b3=(1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)
        
        b2=(c0/4)*(SDF_Aw0**0.5)**(1/(SDF_Aw0))
        
        b1= -( (1/((SDF_Aw0/1000)**(0.5)) ) + (numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1))))) ) * numpy.log(50+1)
        
        k1=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
        k2=1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(1+bhage_Aw)))
        
        N_bh_Aw = SDF_Aw0*k1/k2
    else:
        N_bh_Aw = 0
    
    return N_bh_Aw
    
def densitySb (SDF_Sb0, tage_Sb, SI_bh_Sb):
    
    if SDF_Sb0 > 0:
        c1=-26.3836
        c2=0.166483
        c3=2.738569
        b2=c3
        b3=c3*(SDF_Sb0**(1/SDF_Sb0))
        b1=c1/((((SDF_Sb0/1000)**0.5)+numpy.log(50+1))**c2)
        k1=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+50)))
        k2=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+tage_Sb)))
        
        N_bh_Sb=SDF_Sb0*k1/k2
    else:
        N_bh_Sb = 0
    
    return N_bh_Sb
    
def densitySw (SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw):
  
    if SDF_Sw0 > 0:
        if SDF_Aw0==0:
            z1=0
        elif SDF_Aw0>0:
            z1=1
        c1=-231.617
        c2=1.176995
        c3=1.733601
        b3=c3*(SDF_Sw0**(1/SDF_Sw0))
        b2=c3
        b1=(c1/((numpy.log(SDF_Sw0)+numpy.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000))**0.5))
        k1=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(50+1)))
        k2=1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(1+tage_Sw)))
        
        N_bh_Sw=SDF_Sw0*k1/k2
    else:
        N_bh_Sw = 0
    
    return N_bh_Sw
    
def densityPl (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl, SI_bh_Pl):
    
    if SDF_Pl0 > 0:
        c1=-5.25144
        c2=-483.195
        c3=1.138167
        c4=1.017479
        c5=-0.05471
        c6=4.11215
        if SDF_Aw0==0:
            z1=0
        elif SDF_Aw0>0:
            z1=1
        if SDF_Sw0==0:
            z2=0
        elif SDF_Sw0>0:
            z2=1
        if SDF_Sb0==0:
            z3=0
        elif SDF_Sb0>0:
            z3=1
        k=(1+(c6*(SDF_Pl0**0.5)))/SDF_Pl0 
        
        b3=c4*(SDF_Pl0**k)
        b2=c4/(numpy.sqrt(SDF_Pl0)**c5)
        
        b1=(c1+(z1*(SDF_Aw0/1000)/2) + (z2*(SDF_Sw0/1000)/3) + (z3*(SDF_Sb0/1000)/4)  ) + (c2/((SDF_Pl0**0.5)**c3))
        
        k1=1+numpy.exp(b1 + (b2*numpy.log(SI_bh_Pl)) + (b3*numpy.log(50+1)) )
        k2=1+numpy.exp(b1 + (b2*numpy.log(SI_bh_Pl)) + (b3*numpy.log(1+tage_Pl)) )
        
        N_bh_Pl=SDF_Pl0*k1/k2
    else:
        N_bh_Pl = 0    
    
    return N_bh_Pl
                      
                   


'''
SC is the species composition. It was estimated here using density estimated through bhage, but it could be used using any density, since they should be the same.

BA below is the Basal Area measured in the field and it should be data input into Gypsy 

'''


def SCestimate (N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl):
    N_total = N_bh_Aw + N_bh_Sb + N_bh_Sw + N_bh_Pl
    
    if N_total == 0:
            SC_Aw = 0
            SC_Sw = 0
            SC_Sb = 0
            SC_Pl = 0 
    else:
        SC_Aw = N_bh_Aw/N_total
        SC_Sw = N_bh_Sw/N_total
        SC_Sb = N_bh_Sb/N_total
        SC_Pl = N_bh_Pl/N_total
    return SC_Aw, SC_Sw, SC_Sb, SC_Pl



    
  
def BasalAreaIncrementNonSpatialAw(sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw):
 
    if N_bh_Aw==0:
        BAinc_Aw = 0
        
    if bhage_Aw< 0 :
        raise ValueError ('bhage cannot be negative: %s' %bhage_Aw)
        
    #if BA_Aw< 0 :
        #raise ValueError ('BA_Aw cannot be negative: %s' %BA_Aw)
        

    elif N_bh_Aw>0 and SI_bh_Aw>0:
        a1     =        0.751313
        a2     =        0.018847 
        a3     =        1.143762 
        a4     =        -0.03475 
        a5     =        0.835189 
        
        '''
        k=a4 * numpy.log (0.01+(bhage_Aw/10) )
        k1=(10**(-4)) * a1 * (bhage_Aw**2) * (numpy.exp(-a2*(bhage_Aw**(1/2+a1)))) * (SC_Aw**a5) * ((numpy.log(1+(N0_Aw * numpy.sqrt(1+bhage_Aw) )))**2) * SI_bh_Aw
        k2= ((1+BA_Aw )**a3) * (1+numpy.exp(1 - ((numpy.log(1+SC_Aw**2))/2)    ))
        BAinc_Aw=(k1/k2)+k
        '''
        BAinc_Aw=10**(-4)*a1*(0+bhage_Aw)**2*numpy.exp(-a2*bhage_Aw**(1/2+a1))*SC_Aw**a5*(numpy.log(1+N0_Aw*numpy.sqrt(1+bhage_Aw) ))**2*SI_bh_Aw**1/((1+BA_Aw )**a3 *(1+numpy.exp(1 -numpy.log(1+SC_Aw**2)/2    )))+a4*numpy.log(0.01+bhage_Aw/10)
        
    return BAinc_Aw
    
    


def BAincIter_Aw(sp_Aw, BAinc_AwT, BA_AwT, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, printWarnings = True):
    
    
    acceptableDiff= 0.00001
    BADiffFlag = False
    iterCount = 0 
    BA_Aw = BA_AwT - BAinc_AwT # BA_Aw = best estimate of BA  and BAinc_AwT best estimate of decrement to previous year , ie, at time T-1
    print 'BA_AwT =', BA_AwT, 'BAinc_AwT = ', BAinc_AwT
    while BADiffFlag == False:
        #import pdb; pdb.set_trace()
        BAinc_AwtoT =  BasalAreaIncrementNonSpatialAw (sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw) # based on best estimate of BA at time T-1
        
         
        BA_AwT_est = BA_Aw + BAinc_AwtoT
        print 'kkk', SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw
        
        
        if abs(BA_AwT_est - BA_AwT) < acceptableDiff:           #BA_AwT is known
            BADiffFlag = True
            
        else:
            BA_Aw = (1+ ((BA_AwT - BA_AwT_est)/ BA_AwT)) * BA_Aw
        
        print BAinc_AwtoT, BA_Aw
            
        
           
        iterCount = iterCount + 1
            
        if iterCount == 150 and printWarnings == True:
            print '\n GYPSYNonSpatial.BAincIter_Aw()'
            print ' Slow convergence'
            return BA_Aw, BAinc_AwT
        
    return BA_Aw, BAinc_AwtoT

       
        
        
def BasalAreaIncrementNonSpatialSb (sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb):
    
    
    
    if N_bh_Sb==0:
        BAinc_Sb = 0
        
    if bhage_Sb< 0 :
        raise ValueError ('bhage cannot be negative: %s' %bhage_Sb)
        
    #if BA_Sb< 0 :
        #raise ValueError ('BA_Sb cannot be negative: %s' %BA_Sb)

    elif N_bh_Sb>0 and SI_bh_Sb>0:
        a1      =       0.966285 
        a2      =       0.056315 
        a3      =        0.17191 
        k=(1+((N0_Sb**0.5)*((1+bhage_Sb)**0.5) ) )*(numpy.exp(-(N0_Sb/4)/10000))*(numpy.log(1+SI_bh_Sb)) /  ((1+BA_Sb )**a2)
        
        k1=(10**-4)*a1*(numpy.exp(-a2*bhage_Sb))*(SC_Sb**a3)*(bhage_Sb**(a2+numpy.sqrt(a1)) )
        BAinc_Sb=k*k1
        
              
    return BAinc_Sb
    
    
def BAincIter_Sb(sp_Sb, BAinc_SbT, BA_SbT, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, printWarnings = True):
    
    
    acceptableDiff= 0.00001
    BADiffFlag = False
    iterCount = 0 
    BA_Sb = BA_SbT - BAinc_SbT # BA_Sb = best estimate of BA  and BAinc_AwT best estimate of decrement to previous year , ie, at time T-1
    
    while BADiffFlag == False:
        #import pdb; pdb.set_trace()
        BAinc_SbtoT =  BasalAreaIncrementNonSpatialSb (sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb) # based on best estimate of BA at time T-1
        
         
        BA_SbT_est = BA_Sb + BAinc_SbtoT
        
        
        
        if abs(BA_SbT_est - BA_SbT) < acceptableDiff:           #BA_SbT is known
            BADiffFlag = True
            
        else:
            BA_Sb = (1+ ((BA_SbT - BA_SbT_est)/ BA_SbT)) * BA_Sb
            
            
           
        iterCount = iterCount + 1
            
        if iterCount == 150 and printWarnings == True:
            print '\n GYPSYNonSpatial.BAincIter_Aw()'
            print ' Slow convergence'
            return BA_Sb, BAinc_SbT
        
    return BA_Sb, BAinc_SbtoT
           
    
    
def BasalAreaIncrementNonSpatialSw (sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw):

    if N_bh_Sw==0:
        BAinc_Sw = 0
        
    if bhage_Sw< 0 :
        raise ValueError ('bhage cannot be negative: %s' %bhage_Sw)
        
    if BA_Sw< 0 :
        raise ValueError ('BA_Sw cannot be negative: %s' %BA_Sw)
        
    if N_bh_Sw>0 and SI_bh_Sw>0:
        a1     =        0.089153
        a2     =        0.072171
        a3     =        -0.11483
        a4     =        5.839408
        a5     =        1.753002
        a6     =        0.239521
        if SDF_Aw0==0:
            z1=0
        elif SDF_Aw0>0:
            z1=1
        if SDF_Pl0==0:
            z2=0
        elif SDF_Pl0>0:
            z2=1
        if SDF_Sb0==0:
            z3=0
        elif SDF_Sb0>0:
            z3=1       
            
        k=(a4*z1*numpy.log(1+(SDF_Aw0/10000)) ) + (a5*z2*numpy.log(1+(SDF_Pl0/10000))) + (z3*numpy.log(1+(SDF_Sb0/10000)))
        
        k1=(10**-4)*a1*((a2+bhage_Sw)**2)*((1+bhage_Sw)**((a1**0.5)+a2-a3))*numpy.exp(-a2*bhage_Sw)*(SC_Sw**a6)
        
        k2 = 1+ numpy.exp(1+ k + ( (numpy.log( 1+((N0_Sw**0.5)/10000) )) /2 )  + (a3* numpy.log(1+BA_Sw)) )
        
        m=(numpy.log (1+(N0_Sw*((1+bhage_Sw)**0.5) ))**2)* ((SI_bh_Sw)**0.5) * numpy.exp(-(N0_Sw/10)/10000) 
        
        BAinc_Sw = k1*m/k2
           
        
    return BAinc_Sw


def BAincIter_Sw(sp_Sw, BAinc_SwT, BA_SwT, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, printWarnings = True):
    
    
    acceptableDiff= 0.00001
    BADiffFlag = False
    iterCount = 0 
    BA_Sw = BA_SwT - BAinc_SwT # BA_Sw = best estimate of BA  and BAinc_AwT best estimate of decrement to previous year , ie, at time T-1
    
    while BADiffFlag == False:
        #import pdb; pdb.set_trace()
        BAinc_SwtoT =  BasalAreaIncrementNonSpatialSw (sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw) # based on best estimate of BA at time T-1
        
         
        BA_SwT_est = BA_Sw + BAinc_SwtoT
        
        
        
        if abs(BA_SwT_est - BA_SwT) < acceptableDiff:           #BA_SbT is known
            BADiffFlag = True
            
        else:
            BA_Sw = (1+ ((BA_SwT - BA_SwT_est)/ BA_SwT)) * BA_Sw
            
            
           
        iterCount = iterCount + 1
            
        if iterCount == 150 and printWarnings == True:
            print '\n GYPSYNonSpatial.BAincIter_Aw()'
            print ' Slow convergence'
            return BA_Sw, BAinc_SwT
        
    return BA_Sw, BAinc_SwtoT  
        
        
def BasalAreaIncrementNonSpatialPl(sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl):
    
    if N_bh_Pl==0:
        BAinc_Pl = 0
        
    if bhage_Pl< 0 :
        raise ValueError ('bhage cannot be negative: %s' %bhage_Pl)
        
    if BA_Pl< 0 :
        raise ValueError ('BA_Pl cannot be negative: %s' %BA_Pl)
        
    if N_bh_Pl>0 and SI_bh_Pl>0:
        a1   =          3.923984
        a2   =           0.05752
        a3   =          0.560402
        a4   =          0.672506
        a5   =          -0.00358
        a6   =          0.775765

        if SDF_Aw0==0:
            z1=0
        elif SDF_Aw0>0:
            z1=1
        if SDF_Sw0==0:
            z2=0
        elif SDF_Sw0>0:
            z2=1
        if SDF_Sb0==0:
            z3=0
        elif SDF_Sb0>0:
            z3=1       
            
        k= (z1*numpy.log (1+(SDF_Aw0/1000 ))) + (z2*(numpy.log (1+(SDF_Sw0/1000) ) )/2 )+ (z3* (numpy.log (1+(SDF_Sb0/1000) ) )/2)
                
        k1 = (10**-4)*a1*bhage_Pl* numpy.exp(-a2* bhage_Pl) * ( 1 + ((numpy.log(1+ bhage_Pl))/2) )
        
        k2= 1+numpy.exp( (k/2)+ numpy.log(1+((N0_Pl/3)/10000))  - (a3 * (SC_Pl**0.5)) + (a4*numpy.log(1+BA_Pl ) ))
         
        m1 = (1+a3+(SI_bh_Pl**a6) ) * (N0_Pl**0.5) * numpy.exp(-(N0_Pl/3)/10000)
        
        m2= a5*numpy.log(0.01+(bhage_Pl/10))
        
        BAinc_Pl = (k1*m1/k2)+m2
                   
    return BAinc_Pl
    
    
 
def BAincIter_Pl (sp_Pl, BAinc_PlT, BA_PlT, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, printWarnings = True):
    
    
    acceptableDiff= 0.00001
    BADiffFlag = False
    iterCount = 0 
    BA_Pl = BA_PlT - BAinc_PlT # BA_Pl = best estimate of BA  and BAinc_AwT best estimate of decrement to previous year , ie, at time T-1
    
    while BADiffFlag == False:
        #import pdb; pdb.set_trace()
        BAinc_PltoT =  BasalAreaIncrementNonSpatialPl (sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl) # based on best estimate of BA at time T-1
        
         
        BA_PlT_est = BA_Pl + BAinc_PltoT
        
        
        
        if abs(BA_PlT_est - BA_PlT) < acceptableDiff:           #BA_SbT is known
            BADiffFlag = True
            
        else:
            BA_Pl = (1+ ((BA_PlT - BA_PlT_est)/ BA_PlT)) * BA_Pl
            
            
           
        iterCount = iterCount + 1
            
        if iterCount == 150 and printWarnings == True:
            print '\n GYPSYNonSpatial.BAincIter_Aw()'
            print ' Slow convergence'
            return BA_Pl, BAinc_PlT
        
    return BA_Pl, BAinc_PltoT  


'''
Gross total volume is estimated only using species specific Basal Area and Top height

'''

        
def GrossTotalVolume( BA_Aw, BA_Sb, BA_Sw, BA_Pl, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl):
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
               Tvol_Sb = b1 * (BA_Sb**b2) * (topHeight_Sb**b3)
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
               Tvol_Sw = b1 * (BA_Sw**b2) *  (topHeight_Sw**b3) 
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
    



'''

Merchantable volume only new variables are the stump diameter outside bark, stump height and top diameter inside bark

'''

# to declare variable as double if necessary k_Sb= np.asarray(k_Sb, type = np.float64)









def MerchantableVolumeAw(N_bh_Aw, BA_Aw, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw):
    '''
    I used this if below (and in other functions) to avoid division by zero when density is zero, i.e., when the species is absent in the plot.

    '''
    if N_bh_Aw >0:
            k_Aw = (BA_Aw * 10000 / N_bh_Aw)**0.5
    else:
        k_Aw = 0
    if k_Aw > 0 and  topHeight_Aw>0:
        b0    =         0.993673 
        b1    =         923.5825 
        b2    =         -3.96171 
        b3    =         3.366144 
        b4    =         0.316236 
        b5    =         0.968953 
        b6    =         -1.61247
        k1 = Tvol_Aw * (k_Aw**b0)
        k2 =(b1* (topHeight_Aw**b2) * (StumpDOB_Aw**b3) * (StumpHeight_Aw**b4) * (TopDib_Aw**b5)  * (k_Aw**b6) ) +k_Aw
        MVol_Aw=k1/k2
    else:
        MVol_Aw=0
             
    return MVol_Aw
    

    

   
   

def MerchantableVolumeSb(N_bh_Sb, BA_Sb, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb):   
    if N_bh_Sb >0:
            k_Sb=(BA_Sb * 10000 / N_bh_Sb)**0.5
    else:
        k_Sb = 0
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
               MVol_Sb = (Tvol_Sb * (k_Sb**b0) )/ ((b1* (topHeight_Sb**b2) * (StumpDOB**b3) * (StumpHeight**b4) * (TopDib**b5) * (k_Sb**b6) ) +k_Sb)
    else:
        MVol_Sb=0
        
    return MVol_Sb               
               




def MerchantableVolumeSw(N_bh_Sw, BA_Sw, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw):    
    if N_bh_Sw >0:
            k_Sw=(BA_Sw * 10000 / N_bh_Sw)**0.5
    else: 
        k_Sw= 0          
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
               MVol_Sw = (Tvol_Sw * (k_Sw**b0) ) /   ((b1* (topHeight_Sw**b2) * (sp_Sw[7]**b3) * (sp_Sw[8]**b4) * (sp_Sw[9]**b5) * (k_Sw**b6) ) +k_Sw)
    else:
        MVol_Sw=0               
               
    return MVol_Sw





def MerchantableVolumePl (N_bh_Pl, BA_Pl, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl):  
    if N_bh_Pl > 0:
            k_Pl=(BA_Pl * 10000 / N_bh_Pl)**0.5
    else:
        k_Pl= 0         
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
               MVol_Pl = (Tvol_Pl * (k_Pl**b0) ) / ((b1* (topHeight_Pl**b2) * (sp_Pl[7]**b3) * (sp_Pl[8]**b4) * (sp_Pl[9]**b5) * (k_Pl**b6) ) +k_Pl)
    else:
        MVol_Pl=0
               
    return MVol_Pl
     




