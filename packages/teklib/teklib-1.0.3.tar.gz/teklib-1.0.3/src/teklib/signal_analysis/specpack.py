r"""A python module for spectral analysis

    Functions:
    
    specpack.autospec
    specpack.compspec
    specpack.crosspec
    specpack.gaussiansmooth
    specpack.plotrao
    specpack.plotspec
    specpack.rao
    specpack.specdata
    specpack.specmoment

    """


import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt
import math

###########################################################
###########################################################

def phase_autospectrum(S, seed=None):
    """ Energy auto-spectrum S(f) 
    For wave elevation the units are m*m*s
    """
    np.random.seed(seed)
    phases = np.random.rand(len(S))*2*np.pi
    return S*np.exp(1j*phases)

###########################################################
###########################################################

def autospec(x,t,smooth=False,bw=0.001,welch=False,**kwargs):
    r"""specpack.autospec
        -----------------

        Calculates auto-spectrum of the time series x
        Returns the one-sided auto-spectrum
        
        Option to smooth:
            1.  welch = False : applies a Gaussian smoothing in the pseudo time domain
                smooth = True
                bw = spectral bandwidth of Gaussian

            2.  welch = True : uses scipy.signal welch method. Accepted kwargs are 
                nseg - number of segments (defaults to 30)
                window - defaults to a Gaussian with std 0.25 the segment length


        -----------------

        Input:   x - time series 
                 t - time vector
                 bw - smoothing parameter

        Output:  G_xx - auto-spectrum of x 
                 fz  - corresponding frequency vector

        -----------------"""

    assert(len(x) == len(t)), "time and signal array must be equal"

    # Time and frequency vector characteristics
    dt = t[1]-t[0]
    Nt = len(t)   

    if welch: # use scipy's welch method (removes mean)
        nseg = kwargs["nseg"] if "nseg" in kwargs else 30
        nperseg = len(x) // nseg
        window = kwargs["window"] if "window" in kwargs else sg.windows.gaussian(nperseg,std=nperseg/4)
        n = np.log(nperseg)//np.log(2) + 3  # unsure about this nfft = 2**16 works with test case
        fz, Sxx = sg.welch(x, fs = 1/dt, nperseg = nperseg, window=window, nfft=2**n) 
        return Sxx, fz

    # Remove mean 
    x = x-np.mean(x)

    # zero padding !
    Nn = 2**int(math.ceil(math.log(Nt,2)))
    df = 1/Nn/dt  # zero padded frequency step size  
    fz = np.arange(0, Nn//2)*df

    # Calculate Fourier transform
    X = np.fft.fft(x,Nn)

    # Calculate auto-spectrum
    # The Nt is to normalize the spectrum so it is not a function of r.length 
    # The *2 is to keep the same energy (as we drop half the spectrum)
    # The dt is to convert the power to an energy spectrum
    G_xx =np.abs(X)**2/Nt * 2*dt

    return (gaussiansmooth(G_xx[:Nn//2],fz,bw).real, fz) if smooth else (G_xx[:Nn//2].real,fz) 
    
###########################################################
###########################################################

def crosspec(x, y, t, smooth=False, bw=0.001, welch=False, **kwargs):
    r"""specpack.crosspec
        -----------------
        
        Calculates cross-spectrum of two time series

        -----------------

        Input:     x - Time series 1
                   y - Time series 2
                   t - time vector

        Option to smooth:
            1.  welch = False : applies a Gaussian smoothing in the pseudo time domain
                smooth = True
                bw = spectral bandwidth of Gaussian

            2.  welch = True : uses scipy.signal welch method. Accepted kwargs are 
                nseg - number of segments (defaults to 30)
                window - defaults to a Gaussian with std 0.25 the segment length

        Output:    G_xy - Cross-spectrum of x and y
                   fz  - corresponding frequency vector
                   
        -----------------"""

    assert(len(x) == len(y) == len(t)), "time and signal arrays must be equal length"

    # Time and frequency vector characteristics
    dt = t[1]-t[0]
    Nt = len(t)

    if welch: # use scipy's welch method (removes mean)
        nseg = kwargs["nseg"] if "nseg" in kwargs else 30
        nperseg = len(x) // nseg
        window = kwargs["window"] if "window" in kwargs else sg.windows.gaussian(nperseg,std=nperseg/4)
        n = np.log(nperseg)//np.log(2) + 3  # unsure about this nfft = 2**16 works with test case
        fz, Sxy = sg.csd(x, y, fs = 1/dt, nperseg = nperseg, window=window, nfft=2**n) 
        return Sxy, fz


    # Remove mean
    x = x-x.mean()
    y = y-y.mean()

    # zero padding !
    Nn = 2**int(math.ceil(math.log(Nt,2)))
    df = 1/Nn/dt  # zero padded frequency step size  
    fz = np.arange(0, Nn//2)*df

    # Calculate Fourier transforms
    X = np.fft.fft(x,Nn)
    Y = np.fft.fft(y,Nn)

    # Calculate cross-spectrum (reference autospectra)
    G_xy = X.conjugate()*Y/Nt * 2*dt

    return (gaussiansmooth(G_xy[:Nn//2],fz,bw), fz) if smooth else (G_xy[:Nn//2],fz)


###########################################################
###########################################################

def coherence(x, y, t, smooth=False, bw=0.001, welch=False, spectra=False, **kwargs):
    r"""specpack.coherencec
        -----------------
        
        Calculates coherence of two time series x(t) and y(t)

        -----------------

        Input:     x - Time series 1
                   y - Time series 2
                   t - time vector

        Option to smooth:
            1.  welch = False : applies a Gaussian smoothing in the pseudo time domain
                smooth = True
                bw = spectral bandwidth of Gaussian

            2.  welch = True : uses scipy.signal welch method. Accepted kwargs are 
                nseg - number of segments (defaults to 30)
                window - defaults to a Gaussian with std 0.25 the segment length

        Output:     C_xy - coherence of x and y
                    fz   - corresponding frequency vector

                If spectra = True, also returns the additional fields

                    G_xy - cross-spectrum of x and y
                    G_xx - auto-spectrum of x
                    G_yy - auto-spectrum of y

        -----------------"""
    G_xy, fz = crosspec(x, y, t, smooth=smooth, bw=bw, welch=welch, **kwargs)
    G_xx, fz = autospec(x, t, smooth=smooth, bw=bw, welch=welch, **kwargs)
    G_yy, fz = autospec(y, t, smooth=smooth, bw=bw, welch=welch, **kwargs)
    C_xy = np.where(G_xx*G_yy>0, np.abs(G_xy)**2/(G_xx*G_yy), 0)
    return (C_xy, fz, G_xy, G_xx, G_yy) if spectra else (C_xy, fz)

###########################################################
###########################################################


def rao(x, y, t, phase=True, smooth=False, bw=0.001, welch=False, spectra=False, **kwargs):
    r"""specpack.rao
        -----------------------
       
        Calculates RAO
 
        Uses:    specpack.autospec
                 specpack.crosspec
                 specpack.gaussiansmooth

        -----------------------

        Input:  x - displacement time series
                y - wave time series
                t - corresponding time vector

        Option to smooth:
            1.  welch = False : applies a Gaussian smoothing in the pseudo time domain
                smooth = True
                bw = spectral bandwidth of Gaussian

            2.  welch = True : uses scipy.signal welch method. Accepted kwargs are 
                nseg - number of segments (defaults to 30)
                window - defaults to a Gaussian with std 0.25 the segment length

        Output: H1 - linear x to y transfer function
                fz  - corresponding frequency vector

            If phase = True, returns the complex transfer function H1
            If phase = False, returns the absolute of H1 (aka RAO).

            If spectra = True, also returns the additional fields

                G_xy - cross-spectrum of x and y
                G_xx - auto-spectrum of x
                G_yy - auto-spectrum of y
                C_xy - correlation coefficient of x and y

        -----------------------"""

    C_xy, fz, G_xy, G_xx, G_yy = coherence(x, y, t, smooth=smooth, bw=bw, welch=welch, spectra=True, **kwargs)
    H1 = np.where((C_xy > 0.7) & (G_yy/G_yy.max() > 0.05), G_xy/G_yy if phase else np.sqrt(G_xx / G_yy), 0)
    return (H1, fz, G_xy, G_xx, G_yy, C_xy) if spectra else (H1, fz)


###########################################################
###########################################################



def gaussiansmooth(S,w,s=0.001):
    r"""specpack.gaussiansmooth
        -----------------------
       
        Spectral smoothing by convolving the raw spectrum 
        with a Gaussian window in frequency domain.
        Actual computation performed in "time"-domain 
        to avoid the convolution integral.

        Steps:
        1) Calculate the Fourier transform $\hat{S}(t)$ of the 
           raw spectrum $S(\omega)$
        2) Multiply $\hat{S}(t)$ by $\hat{G}(t)=\exp{-\omega^2 t^2/2}$
        3) The smoothed spectrum is the inverse Fourier transform of
           $\hat{S}(t)\hat{G}(t)$

        -----------------------

        Input:  S  - raw spectrum
                w  - corresponding frequency vector [Hz]
                s  - stdev of Gaussian smoothing function [Hz]

        Output: Ss - Smoothed spectrum

        -----------------------"""

    # Test if raw spectrum is real of complex
    complexInputFlag = 1 if any(S.imag!=0) else 0

    # Frequency vector characteristics
    Nw = len(w)
    dw = w[1]-w[0]
    
    # Add zeros to remove edge effects (FFT/periodicity)
    Nzeros = 2*math.floor(float(s)/dw)
    S2 = np.zeros([2*Nzeros+len(S)], np.complex) #float)
    S2[Nzeros:Nzeros+len(S)] = S
    
    if Nw%2!=0: S2=S2[0:-1]
    N2 = len(S2)
    
    # Define "time" vector
    dt = 2.*np.pi/N2/dw
    t = np.arange(-(N2/2.)*dt,((N2/2.)-1)*dt+dt,dt)
    
    # Gaussian window in time domain
    G = np.exp(-(s**2)*(t**2)/2.)
   
    # Smoothing
    Shat = np.fft.fftshift(np.fft.fft(S2))
    Ss   = np.fft.ifft(np.fft.ifftshift(Shat*G))

    # Remove imaginary residual only if input was real
    if complexInputFlag==1:
        SS = Ss.real
    
    return Ss[Nzeros:Nzeros+len(S)]



###########################################################
###########################################################




def plotspec(fz,Ss,xmax,dof,dim,showflag=0,filename=0,xmin=0,title=''):

    """specpack.plotspec
       -----------------

       Plotting of auto-spectra with scaling as in Plotit

       -----------------

       Input:   fz       - frequency vector [Hz]
                Ss       - auto-spectrum
                xmax     - max frequency in plot
                dof      - name of dof
                dim      - dimension of dof
                showflag - if 1, then figure is shown
                filename - if 0, then nothing is done
                           otherwise, figure is saved as filename.png
                xmin     - min frequency in plot, default is 0
                title    - plot title, default is ''

       Output:  Optional show() of figure
                Optional savefig() of figure

       -----------------"""
    
    plt.figure()
    plt.clf()
    plt.plot(fz,Ss,linewidth=2.0)
    ymax = max(1.05*Ss)
    plt.axis([xmin,xmax,0,ymax])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('%s auto-spectrum [%s$^2$s]' % (dof,dim))
    plt.grid()
    plt.title(title)
    if filename!=0:
        plt.savefig(filename+'_autospec')
    if showflag==1:
        plt.show()
    

    plt.close()



###########################################################
###########################################################




def plotRAO(fz,Ss,xmax,label,showflag,filename,axisflag=0,timeflag=0,xmin=0,title=''):

    """specpack.plotRAO
       -----------------

       Plotting of RAO
       
       vak 06.05.2011

       -----------------

       Input:   fz       - frequency vector [Hz]
                RAO      - RAO to be plotted
                xmax     - max value on x-axis
                showflag - if 1, then figure is shown
                filename - if 0, then nothing is done
                           otherwise, figure is saved as filename_RAO.png
                axisflag - if 0, do not plot RAO for frequencies 
                                 lower than 0.025 Hz
                           if 1, plot RAO for low frequencies as well
                timeflag - if 0, plot against frequency
                           if 1, plot against time
                           default is 0
                xmin     - min frequency in plot, default is 0
                title    - plot title, default is ''
                           

       Output:  Optional show() of figure
                Optional savefig() of figure

       -----------------"""
    
    plt.figure()
    plt.clf()

    if axisflag==0:
        minfreq = 0.025    
        ind_low = plt.find(fz>minfreq)[0]
    elif axisflag==1:
        ind_low = 1

    ind_top = len(Ss)
    if len(plt.find(fz<xmax)): ind_top = plt.find(fz<xmax)[-1]


    if timeflag==0:
        plt.plot(fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0)
        plt.xlabel('Frequency [Hz]')
    elif timeflag==1:
        plt.plot(1/fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0)
        plt.xlabel('Period [s]')

    ymax = max(1.05*Ss[ind_low:ind_top])
    plt.axis([xmin,xmax,0,ymax])
    plt.ylabel(label)
    plt.title(title)
    plt.grid()    
    if filename!=0:
        plt.savefig(filename+'_RAO')
    if showflag==1:
        plt.show()

    plt.close()

###########################################################
###########################################################


def plotspec(fz,Ss,xmax,label,showflag,filename,axisflag=0,timeflag=0,xmin=0,title=''):

    """specpack.plotRAO
       -----------------

       Plotting of RAO
       
       vak 06.05.2011

        Modifications:
        tek 13.12.2011 - single-sided returned
       -----------------

       Input:   fz       - frequency vector [Hz]
                spec      - spec to be plotted
                xmax     - max value on x-axis
                showflag - if 1, then figure is shown
                filename - if 0, then nothing is done
                           otherwise, figure is saved as filename_spec.png
                axisflag - if 0, do not plot spec for frequencies 
                                 lower than 0.025 Hz
                           if 1, plot spec for low frequencies as well
                timeflag - if 0, plot against frequency
                           if 1, plot against time
                           default is 0
                xmin     - min frequency in plot, default is 0
                title    - plot title, default is ''
                           

       Output:  Optional show() of figure
                Optional savefig() of figure

       -----------------"""
    
    plt.figure()
    plt.clf()

    if axisflag==0:
        minfreq = 0.025    
        ind_low = plt.find(fz>minfreq)[0]
    elif axisflag==1:
        ind_low = 1

    ind_top = len(Ss)
    if len(plt.find(fz<xmax)): ind_top = plt.find(fz<xmax)[-1]


    if timeflag==0:
        plt.plot(fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0)
        plt.xlabel('Frequency [Hz]')
    elif timeflag==1:
        plt.plot(1/fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0)
        plt.xlabel('Period [s]')

    ymax = max(1.05*Ss[ind_low:ind_top])
    plt.axis([xmin,xmax,0,ymax])
    plt.ylabel(label)
    plt.title(title)
    plt.grid()    
    if filename!=0:
        plt.savefig(filename+'_spec')
    if showflag==1:
        plt.show()

    plt.close()



###########################################################
###########################################################

def specdata(x,t,s=0.001):

    """specpack.specdata
       -------------------

       Summary of spectral data
       
       Uses:    specpack.autospec
                specpack.gaussiansmooth
                specpack.specmoment

       -------------------

       Input:  x - displacement time series
               t - corresponding time vector
               s - smoothing parameter

       Output: M0      - 0th spectral moment 
               M1      - 1st spectral moment 
               M2      - 2nd spectral moment 
               M4      - 4th spectral moment 
               T1      - energy average period
               T2      - average zero crossing period
               peakper - spectral peak period
               H       - significant value


       -----------------"""
    # Spectral moments
    M0 = specmoment(x,t,0,s)
    M1 = specmoment(x,t,1,s)
    M2 = specmoment(x,t,2,s)
    M4 = specmoment(x,t,4,s)

    # Periods
    #T1 = 2*np.pi*M0/M1 
    #T2 = 2*np.pi*np.sqrt(M0/M2)

    T1 = M0/M1 
    T2 = np.sqrt(M0/M2)

    # Spectral peak period
    [asp,fz] = autospec(x,t)
    asp_s = gaussiansmooth(asp,fz,s)
    peakper = float(1./fz[np.nonzero(asp_s==asp_s.max())])

    # Significant value
    H  = 4*np.sqrt(M0)

    return M0,M1,M2,M4,T1,T2,peakper,H

###########################################################
###########################################################

def specmoment(x,t,n,s):
    
    """specpack.specmoment
       -------------------

       Calculation of spectral moments based on a smoothed spectrum
       
       Uses:    specpack.autospec
                specpack.gaussiansmooth

       -------------------

       Input:  x - displacement time series
               t - corresponding time vector
               n - order of moment
               s - smoothing parameter

       Output: M - nth spectral moment 

       -----------------"""
    
    [asp,fz] = autospec(x,t) # single-sided!

    asp_s = gaussiansmooth(asp,fz,s)
    
    # Use trapezoidal quadrature from numpy 

    N = min(len(fz), len(asp_s))
    M = np.trapz(fz[:N]**n*asp_s[:N],fz[:N])

    return M


###########################################################
###########################################################



def compspec(fz1,Ss1,fz2,Ss2,fw,Sw,lab1,lab2,xmax,dof,dim,
            showflag=0,filename=0,legend=None,
            xmin=0,title='',fz_WADAM=None, Ss_WADAM=None, **kwargs):

    """specpack.compspec
       -----------------

       Plotting of two auto-spectra with scaling as in Plotit
       
       vak 06.05.2011

        Modifications:
        tek 13.12.2011 - single-sided returned
       -----------------

       Input:   fz1      - frequency vector [Hz] of spectrum 1
                Ss1      - auto-spectrum 1
                fz2      - frequency vector [Hz] of spectrum 2
                Ss2      - auto-spectrum 2
                xmax     - max frequency in plot
                dof      - name of dof
                dim      - dimension of dof
                showflag - if 1, then figure is shown
                filename - if 0, then nothing is done
                           otherwise, figure is saved as filename.png
                legend   - default is None
                xmin     - min frequency in plot, default is 0
                title    - plot title, default is ''

       Output:  Optional show() of figure
                Optional savefig() of figure

       -----------------"""
    
    plt.figure()
    plt.clf()
    p1 = plt.plot(fz1,Ss1,linewidth=2.0, label=lab1)
    p2 = plt.plot(fz2,Ss2,linewidth=2.0, label=lab2)
    ymax = max(max(1.05*Ss1),max(1.05*Ss2))
    plt.axis([xmin,xmax,0,ymax])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('%s auto-spectrum [%s$^2$s]' % (dof,dim))
    color = plt.cm.rainbow(np.linspace(0,1,len(kwargs)))
    for i, (k, v) in enumerate(kwargs.items()):
        plt.axvline(v, label=k, linestyle='--', color=color[i])
    # Add the response spectrum based on the WADAM RAOs
    if fz_WADAM is not None:
        plt.plot(fz_WADAM, Ss_WADAM, label="WADAM (WF only)")
    plt.title(title)
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax2.plot(fw, Sw, label="wave", linestyle='--', color='k')
    ax2.set_ylabel("Wave Spectrum ($m^2s$)", color='k')
    ax2.set_ylim(0)
    l1, h1 = ax1.get_legend_handles_labels()
    l2, h2 = ax2.get_legend_handles_labels()
    plt.legend(l1+l2, h1+h2, loc=0)
    plt.grid()

    if legend is not None:
        plt.legend((legend))
    if filename!=0:
        plt.savefig(filename+'_compautospec')
    if showflag==1:
        plt.show()
    
    plt.close()



#######################################################################################
#######################################################################################

def compareRAOs(wsimo,wmodel,xsimo,xmodel,tsimo,tmodel,filename,rao_diff=None,
    periods_diff=None,diff_label="WADAM",title=None,xmin=0,xmax=30.,
    testno=None,hertz=False,ylabel="", no_simo=False):
    fig, ax1 = plt.subplots()
    rao_sim, fz_sim = rao(xsimo, wsimo, tsimo, smooth=True, bw=0.001)
    rao_test, fz_test = rao(xmodel, wmodel, tmodel, smooth=True, bw=0.001)
    ix = np.nonzero(rao_test)
    ax1.plot(fz_test[ix] if hertz else 1/fz_test[ix], np.abs(rao_test[ix]), label=f"Test {testno if testno is not None else ''}")
    ix = np.nonzero(rao_sim)
    if not no_simo:
        ax1.plot(fz_sim[ix] if hertz else 1/fz_sim[ix], np.abs(rao_sim[ix]), label=f"SIMO")
    if rao_diff is not None: ax1.plot(1/periods_diff if hertz else periods_diff, np.abs(rao_diff), label=diff_label)
    if title is not None: fig.suptitle(title)
    ax1.set_xlabel("Wave " + "frequency [Hz]" if hertz else "period [s]")
    ax1.set_ylabel(ylabel)
    ax1.set_xlim(xmin,xmax)
    ax1.set_ylim(0)
    ax1.legend(loc=0)
    plt.savefig(filename + "_RAO.png")
    plt.close(fig)


def compareRAOsWisting(wsimo,wmodel,xsimo,xmodel,tsimo,tmodel,filename=None,rao_diff=None,
    periods_diff=None,diff_label="WADAM",title=None,xmin=0,xmax=30.,
    testno=None,hertz=False,ylabel="",axs=None, index=0, no_simo=False, naxes=3, figsize=(12,4)):
    if axs is None:
        fig, ax1 = plt.subplots(ncols=naxes, figsize=figsize)
        plt.subplots_adjust(wspace=0.3)
    else:
        fig, ax1 = plt.gcf(), axs
    rao_sim, fz_sim = rao(xsimo, wsimo, tsimo, smooth=True, bw=0.001)
    rao_test, fz_test = rao(xmodel, wmodel, tmodel, smooth=True, bw=0.001)
    ix = np.nonzero(rao_test)
    ax1[index].plot(fz_test[ix] if hertz else 1/fz_test[ix], np.abs(rao_test[ix]), label=f"Test {testno if testno is not None else ''}")
    ix = np.nonzero(rao_sim)
    if not no_simo:
        ax1[index].plot(fz_sim[ix] if hertz else 1/fz_sim[ix], np.abs(rao_sim[ix]), label=f"SIMO")
    if rao_diff is not None: ax1[index].plot(1/periods_diff if hertz else periods_diff, np.abs(rao_diff), label=diff_label)
    if title is not None: fig.suptitle(title)
    ax1[index].set_xlabel("Wave " + "frequency [Hz]" if hertz else "period [s]")
    ax1[index].set_ylabel(ylabel)
    ax1[index].set_xlim(xmin,xmax)
    ax1[index].set_ylim(0)
    if index==0: ax1[index].legend(loc=0)
    if filename is None: return ax1
    plt.savefig(filename + "_RAO.png")
    plt.close(fig)


def compRAO(fz,Ss,fzW,SsW,xmax,label,showflag,filename,axisflag=0,timeflag=0,xmin=0,title=''):

    """specpack.plotRAO
       -----------------

       Plotting of RAO
       
       -----------------

       Input:   fz       - frequency vector [Hz]
                RAO      - RAO to be plotted
                xmax     - max value on x-axis
                showflag - if 1, then figure is shown
                filename - if 0, then nothing is done
                           otherwise, figure is saved as filename_RAO.png
                axisflag - if 0, do not plot RAO for frequencies 
                                 lower than 0.025 Hz
                           if 1, plot RAO for low frequencies as well
                timeflag - if 0, plot against frequency
                           if 1, plot against time
                           default is 0
                xmin     - min frequency in plot, default is 0
                title    - plot title, default is ''
                           

       Output:  Optional show() of figure
                Optional savefig() of figure

       -----------------"""
    
    plt.figure()
    plt.clf()

    if axisflag==0:
        minfreq = 0.025    
        ind_low = plt.find(fz>minfreq)[0]
    elif axisflag==1:
        ind_low = 1

    ind_top = len(Ss)
    if len(plt.find(fz<xmax)): ind_top = plt.find(fz<xmax)[-1]


    if timeflag==0:
        plt.plot(fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0,label='Model Test')
        plt.plot(fzW, SsW, label='WAMIT')
        plt.xlabel('Frequency [Hz]')
    elif timeflag==1:
        plt.plot(1/fz[ind_low:ind_top],Ss[ind_low:ind_top],linewidth=2.0,label='Model Test')
        plt.plot(fzW, SsW, label='WAMIT')
        plt.xlabel('Period [s]')

    ymax = max(1.05*Ss[ind_low:ind_top])
    plt.axis([xmin,xmax,0,ymax])
    plt.ylabel(label)
    plt.title(title)
    plt.legend(loc=0)
    plt.grid()    
    if filename!=0:
        plt.savefig(filename+'_RAO')
    if showflag==1:
        plt.show()

    plt.close()




#################


def wave_ts(S, t, seed=None, RAS=False):
    """
    Generates a wave time series from a wave spectrum using random phases, where
    S(w) is a function that returns the spectrums value at w. If RAS is True, random
    amplitudes at each frequency are drawn from the respective Rayleigh distribution

    TODO: Issue to resolve with RAS setup. 
    The difference betweem the correct and applied approach for RAS is one uses a
    factor of sqrt(2/pi) = 0.79 and the other uses a factor sqrt(1/2) = 0.71
    

    Example of use:
    ===============
    from wafo.spectrum.models import Torsethaugen
    from teklib.signal_analysis.specpack import wave_ts

    S = Torsethaugen(Hm0=7, Tp=10) 
    dt = 0.2 # s
    t = np.arange(0,3*60*60*5)*dt
    eta = wave_ts(S, t)
    """    

    # Establish one-sided frequency array
    dt, N, df = t[1] - t[0], len(t), 1/len(t)/(t[1]-t[0])
    fz = np.fft.fftfreq(len(t), d=dt)[:N//2]
    assert(fz[1]-fz[0] == df), "df mismatch"

    # Generate spectral amplitudes 
    Sf = S(2*np.pi*fz)*2*np.pi
    np.random.seed(seed) # Seed option for reproducibility
    phases = np.random.rand(len(Sf))*2*np.pi
    mean_ap = np.sqrt(2*Sf*df)
    mode_ap = np.sqrt(2/np.pi)*mean_ap
    #scale = np.sqrt(4*Sf*df/(4-np.pi)) # Using paper with 2*Sf*df as variance and wiki's scale relation
    ap = np.random.rayleigh(mode_ap) if RAS else mean_ap # this RAS should be correct
    ap = np.random.rayleigh(1/2**0.5*mean_ap) if RAS else mean_ap # but this hits Hs
    #ap = np.random.rayleigh(scale) if RAS else mean_ap # but this hits Hs
    ap = ap*np.exp(1j*phases)

    # ifft back to generate a wave elevation
    eta = np.fft.ifft(ap*len(t), n=len(t)) 



    return eta.real

