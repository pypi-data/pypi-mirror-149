########################################################################
# program: rainflow.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.4
# date: October 4, 2013
# description:  
#
# Modified version: tike@statoil.com
# Modifications: only input
#
#    - to avoid function calls to tompy
#    - to facilitate command line processing
#    - to provide a calling function for integrating into other programs
#
#  ASTM E 1049-85 (2005) Rainflow Counting Method
#              
########################################################################

import sys
import numpy as np
import pylab as plt
from time import time

########################################################################

class Rainflow:

    def __init__(self):
    
        self.b=[]
        self.ymax=0.
        self.num=0



    @classmethod 
    def rainflow_input(cls,self,data,submean=False):
        self.b=data
        self.num = len(self.b)
        if submean: self.b-=np.mean(self.b)  

   
    @classmethod    
    def rainflow_bins(cls,self,B,kv,hold,sum,nbins):        
        
        L=np.r_[0,np.linspace(0,100,nbins+1)]
        C=np.zeros(nbins+2,'f')

        AverageMean = np.zeros(nbins+2,'f')
        MaxPeak     = np.zeros(nbins+2,'f')
        MinValley   = np.zeros(nbins+2,'f')
        MaxAmp      = np.zeros(nbins+2,'f')
        AverageAmp  = np.zeros(nbins+2,'f')

        for ijk in range (1,nbins+2):
    
            L[ijk]*=self.ymax/100.
    
            MaxPeak[ijk]=-1.0e+20
            MinValley[ijk]= 1.0e+20

            MaxAmp[ijk]=-1.0e+20

        kv-=1


        for i in range (0,kv+1):
             Y=B[i][0]
          
             for ijk in range (nbins,0,-1):
         
                if(Y>=L[ijk] and Y<=L[ijk+1]):
                    
                    C[ijk]+=B[i][1]
            
                    AverageMean[ijk]+=B[i][1]*(B[i][3]+B[i][2])*0.5  # weighted average    

                    if(B[i][3]>MaxPeak[ijk]):   MaxPeak[ijk]   = B[i][3]
                    if(B[i][2]>MaxPeak[ijk]):   MaxPeak[ijk]   = B[i][2]
                    if(B[i][3]<MinValley[ijk]): MinValley[ijk] = B[i][3]
                    if(B[i][2]<MinValley[ijk]): MinValley[ijk] = B[i][2]
                    if(Y>MaxAmp[ijk]): MaxAmp[ijk]=Y

                    AverageAmp[ijk]+=B[i][1]*Y*0.5

                    break

        for ijk in range (1,nbins+2):

            if(C[ijk]>0):
                AverageMean[ijk]/=C[ijk]
                AverageAmp[ijk]/=C[ijk]
              
            if(C[ijk]<0.5):
                AverageMean[ijk]=0.    
                AverageAmp[ijk]=0.       
                MaxPeak[ijk]=0.            
                MinValley[ijk]=0.         
                MaxAmp[ijk]=0.            
        
            MaxAmp[ijk]/=2.


        N = nbins
        midrange  = np.r_[[(L[i]+L[i+1])/2. for i in range(1,nbins+1)]]
        widths    = np.r_[[L[i+1]-L[i] for i in range(1,nbins+1)]]
        numcycles = np.r_[C[1:N+1]]


        print('\n  Amplitude = (peak-valley)/2 \n\n')
#*****************************************************************************

        print("          Range            Cycle       Ave      Max     Ave     Min       Max")
        print("         (units)           Counts      Amp      Amp     Mean    Valley    Peak")

        for i in range (13,0,-1):
            print(("  %8.2f to %8.2f\t%8.1f\t%6.4g\t%6.4g\t%6.4g\t%6.4g\t %6.4g" \
             %(L[i],L[i+1],C[i],AverageAmp[i],MaxAmp[i],AverageMean[i],MinValley[i],MaxPeak[i])))

        yf=self.ymax

        print(("\n\n  Total Cycles = %g  hold=%d  NP=%d ymax=%g" %(sum,hold,self.num,yf)))	

        return midrange, widths, numcycles
            
########################################################################

    def rainflow_core(self, data, nbins, ymax=False):
        
        t0 = time()

        Rainflow.rainflow_input(self, data, False)
                 
########################################################################

        y=np.zeros(self.num,'f')
        a=np.zeros(self.num,'f')
        B=np.zeros((self.num,4),'f')

        y=self.b
        k=0
        a[0]=y[0]

        k=1

        for i in range (1,(self.num-1)):
            
            slope1=(  y[i]-y[i-1])
            slope2=(y[i+1]-y[i])

            if((slope1*slope2)<=0):
                a[k]=y[i]
                k+=1
                 
            
        last_a=k        
        hold=last_a        
        a[k]=y[self.num-1]

        mina=min(a)
        maxa=max(a)


        if sys.version_info[0] == 2:
            nmm=int(maxa-mina)+1

        if sys.version_info[0] == 3:
            nmm=int(maxa-mina)+1

	
        i=0
        j=1

        sum=0
        kv=0

        self.ymax=-1.0e+20

        print (" ")

        aa=a.tolist()

        nkv=0

        print ("\n percent completed \n")

        ijk=0
        LLL=int(0.2*float(hold/2))

        while(1):
        
            Y=abs(aa[i]-aa[i+1])
            X=abs(aa[j]-aa[j+1])
    
            if(X>=Y and Y>0):		
                if(Y>self.ymax):
                    self.ymax=Y
             
                if(i==0):		
                    
                    sum+=0.5
                    B[kv][3]=aa[i+1]
                    B[kv][2]=aa[i]
                    B[kv][1]=0.5
                    B[kv][0]=Y
                    kv+=1
                    aa.pop(i)
                    last_a-=1
                    i=0
                    j=1    
                
                else:      
                    sum+=1
                    B[kv][3]=aa[i+1]
                    B[kv][2]=aa[i]
                    B[kv][1]=1.
                    B[kv][0]=Y
                    kv+=1	

                    aa.pop(i+1)
                    aa.pop(i)                
                
                    i=0
                    j=1

                    last_a-=2
            
                    nkv+=1

                    ijk+=1  
  
                    if(ijk==LLL):
                        pr=(sum/(hold/2))*100.
                        print((" %3.0f" %(pr)))
                        ijk=0               
             	    
            else:
                i+=1
                j+=1
                
            if((j+1)>last_a):
                break                
 
#### 
 
        for i in range (0,last_a):
	
            Y=(abs(aa[i]-aa[i+1]))

            if(Y>0):
		
                sum+=0.5
                B[kv][3]=aa[i+1]
                B[kv][2]=aa[i]
                B[kv][1]=0.5
                B[kv][0]=Y
        
                kv+=1
		
                if(Y>self.ymax):
                   self.ymax=Y
 
        if ymax: self.ymax = ymax
        print((" ymax=%8.4g " %self.ymax))


        midrange, widths, numcycles = Rainflow.rainflow_bins(self,B,kv,hold,sum,nbins)
        return midrange, widths, numcycles

  
###############################################################################
  
class CDI:

    def __init__(self):
    
        pass
   
    def fatigue(self,B,b):   
        
        D=0
        
        kv=B.shape[0]

        for i in range (0,kv):
       
            Y=B[i][0]
            D+=B[i][1]*((Y/2.)**b)
       
        print(("\n D=%8.4g \n" %D))

###############################################################################        

