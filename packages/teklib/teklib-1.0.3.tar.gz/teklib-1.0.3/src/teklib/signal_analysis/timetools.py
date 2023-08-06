r"""A python module with various tools for time series

    Functions:
    
    timetools.find_peaks
    timetools.resample
    timetools.window
    timetools.make_plotMT
    timetools.allstats
    

    """


import numpy as np
import pylab as plt
import math
from scipy import stats as scipystats



###########################################################
###########################################################

def find_peaks(z:np.ndarray, global_peaks:bool=False, maxima:bool=True):
    """ 
    Returns a numpy (index) array to the turning points in a time series 'z'
    If maxima == True/False, the function returns the indices to the maxima/minima respectively
    If global_peaks=True/False, the function returns the indices to the global/local peaks
    """
    from scipy.signal import argrelextrema
    if global_peaks:
        z0 = z - z.mean()
        ix, = np.nonzero(np.r_[0, np.diff((z0 > 0)*1)]) # all the zero-crossing point
        argfunc = np.argmax if maxima else np.argmin
        up_first = True if z0[0] < 0 else False # check if the first zero-crossing is an up-crossing
        k = 0 if up_first and maxima or not up_first and not maxima else 1
        return np.ix_([i + argfunc(z[i:j]) for i, j in zip(ix[k:-1:2], ix[k+1::2])])
    else:
        return argrelextrema(z - z.mean(), np.greater if maxima else np.less)
    


def resample(x,told,dtnew):
    r"""timetools.resample
        -----------------
    
        Resamples the time series x over a new time vector
        
        vak 19.05.2011

        -----------------

        Input:   x     - time series 
                 told  - old time vector
                 dtnew - new time step                 

        Output:  xnew  - resampled time series
                 tnew  - corresponding time vector

        -----------------"""

    # Time vector characteristics
    #dtold = told[1]-told[0]
    tnew = np.arange(told[0],told[-1]+dtnew/2.,dtnew)
    #print len(tnew), len(told), len(x)
    
    # Linearly interpolate x over tnew
    xnew = np.interp(tnew,told,x)

    return xnew, tnew



###########################################################
###########################################################

    
def plot_ts(title,x0,y0,label,unit,tofile):
    plt.figure(figsize=(12,8))
    plt.axes([0.15,0.1,0.65,0.75])
    for i in range(0,3):

        plt.subplot(311)
        plt.suptitle(title)
        plt.plot(x0,y0,'r',label=label)
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(0.+3000*i,1000.+3000*i)
        plt.legend(loc=0)
        
        plt.subplot(312)
        plt.plot(x0,y0,'r',label=label)
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(1000.+3000*i,2000.+3000*i)
        
        plt.subplot(313)
        plt.plot(x0,y0,'r',label=label)
        plt.xlabel('time [s]')
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(2000.+3000*i,3000.+3000*i)
        plt.savefig(tofile + '_time%d.png' % i)
        plt.clf()





###########################################################
###########################################################



    
def make_plotMT(title,x0,y0,x1,y1,label1,label2,unit,tofile):
    plt.figure(figsize=(12,8))
    plt.axes([0.15,0.1,0.65,0.75])
    for i in range(0,5):

        plt.subplot(311)
        plt.title(title)
        plt.plot(x0,y0,'r',label=label1)
        plt.plot(x1,y1,'k',label=label2)
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(0.+3000*i,1000.+3000*i)
        plt.legend(loc=0)
        
        plt.subplot(312)
        plt.plot(x0,y0,'r',label=label1)
        plt.plot(x1,y1,'k',label=label2)
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(1000.+3000*i,2000.+3000*i)
        
        plt.subplot(313)
        plt.plot(x0,y0,'r',label=label1)
        plt.plot(x1,y1,'k',label=label2)
        plt.xlabel('time [s]')
        plt.ylabel('[%s]' % unit)
        plt.grid()
        plt.xlim(2000.+3000*i,3000.+3000*i)
        plt.savefig(tofile + '_time%d.png' % i)
        plt.clf()



###########################################################
###########################################################



def allstats(x,t):
    r"""timetools.allstats
        -----------------

        Returns "all" statistics similar as for model tests
        
        vak 06.05.2011

        -----------------

        Input:   x - time series 
                 t - time vector

        Output:  ? - ?

        -----------------"""

    x_mean    = x.mean()
    x_max     = x.max()
    x_min     = x.min()
    x_std     = x.std()
    x_nmax    = 0.
    x_nmin    = 0.
    x_nmcross = 0.
    x_maxpp   = 0.
    x_sgnpp   = 0.
    x_sgnmax  = 0.
    x_sgnmin  = 0.
    x_skew    = scipystats.skew(x)
    x_kurt    = scipystats.kurtosis(x)
    x_estmax  = 0.
    x_estmin  = 0.

    return x_mean,x_max,x_min,x_std,x_nmax,x_nmin,x_nmcross,x_maxpp,x_sgnpp,x_sgnmax,x_sgnmin,x_skew,x_kurt,x_estmax,x_estmin




###########################################################
###########################################################


def window(x,t,t0,duration,dt=None):
    r"""timetools.window
        -----------------
    
        Windows the time series x(t) between t0 <= t < t1
        where t1 = t0 + duration. 

        The function offers an optional resample to a 
        time step dt.

        tek 17.06.2010

        -----------------

        Input:   x - numpy time series array
        Output:  tuple(X(T), T) 
                  X(T) - windowed time series
                  T    - corresponding time vector
        -----------------"""

    ix =  np.nonzero(t > t0)
    x, t = x[ix], t[ix]
    ix =  np.nonzero(t < t0 + duration)
    x, t = x[ix], t[ix]
    if dt is not None: 
        rt = np.arange(t[0],t[-1],dt)
        return np.interp(rt, t, x), rt
    else:
        return x, t
