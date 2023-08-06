import numpy as np
import matplotlib.pyplot as plt
from .timetools import find_peaks


def empirical_cdf(n:int, kind:str='mean'):
    """
    Empirical cumulative distribution function given a sample size.

    Parameters
    ----------
    n : int
        sample size
    kind : str, optional
        - 'mean':  ``i/(n+1)`` (aka. Weibull method)
        - 'median' ``(i-0.3)/(n+0.4)``
        - 'symmetrical': ``(i-0.5)/n``
        - 'beard': ``(i - 0.31)/(n + 0.38)`` (Jenkinson's/Beard's method)
        - 'gringorten': ``(i - 0.44)/(n + 0.12)`` (Gringorten's method)

    Returns
    -------
    array
        Empirical cumulative distribution function

    Notes
    -----
    Gumbel recommended the following quantile formulation ``Pi = i/(n+1)``.
    This formulation produces a symmetrical CDF in the sense that the same
    plotting positions will result from the data regardless of
    whether they are assembled in ascending or descending order.

    Jenkinson's/Beard's method is based on the "idea that a natural
    estimate for the plotting position is the median of its probability
    density distribution".

    A more sophisticated formulation ``Pi = (i-0.3)/(n+0.4)`` approximates the
    median of the distribution free estimate of the sample variate to about
    0.1% and, even for small values of `n`, produces parameter estimations
    comparable to the result obtained by maximum likelihood estimations
    (Bury, 1999, p43)

    The probability corresponding to the unbiased plotting position can be
    approximated by the Gringorten formula in the case of type 1 Extreme
    value distribution.

    References
    ----------
    1. `Plotting positions <http://en.wikipedia.org/wiki/Q%E2%80%93Q_plot>`_, About plotting positions
    """

    n = float(n)
    i = np.arange(n) + 1
    if kind == 'mean':
        f = i / (n + 1.)
    elif kind == 'median':
        f = (i - 0.3) / (n + 0.4)
    elif kind == 'symmetrical':
        f = (i - 0.5) / n
    elif kind == 'beard':
        f = (i - 0.31) / (n + 0.38)
    elif kind == 'gringorten':
        f = (i - 0.44) / (n + 0.12)
    else:
        raise ValueError("Distribution type must be either 'mean','median','symmetrical','beard','gringorten'")

    return f


def fit_Weibull(x:np.ndarray,t:np.ndarray,maxima:bool=True, t0:float=0, duration:float=3, 
                savefig:bool=False, figname:str="weibull.png"):
    """fits a Weibull distribution to either the maxima of minima of a timeseries x(t)

    Args:
        x (np.ndarray): timeseries x(t)
        t (np.ndarray): time in seconds
        maxima (bool, optional): fit to maxima if True, and minima if False. Defaults to True.
        t0 (float, optional): start time for windowing x(t) in seconds. Defaults to 0.
        duration (float, optional): duration of event in hours. Defaults to 3.
        savefig (bool, optional): set True to save the figure. If False figure axes is returned. Defaults to False.
        figname (str, optional): name of figure is savefig=True. Defaults to "weibull.png".

    Returns:
        tuple: 
            <duration>-hour sample extreme,
            <duration>-hour estimated extreme (Weibull fit)
            <duration>-hour mpm extreme (should equate to estimate extreme)
            <duration>-hour expected extreme
            <duration>-hour 90th percentile extreme
            if savefig=False: figure axes
    """
    from qats.stats.weibull import Weibull
    from scipy.stats import gumbel_l, gumbel_r, weibull_max, weibull_min, rayleigh
    sign = 1 if maxima else -1
    x = x*sign # flip space if minima
    # Window the time series
    ix = (t>t0) & (t<t0+duration*60*60)
    x, t = x[ix], t[ix]
    # helper function to deal with minima
    correct_space = lambda x, maxima: x if maxima else -x 
    # find peaks 
    ix = find_peaks(x, global_peaks=True)
    # fit a Weibull distribution. Use qats for now
    weib_qats = Weibull.fit(data=x[ix])
    # get the Weibull params
    loc, scale, shape = weib_qats.params  # maxima_space
    # determine simulation hours (not duration for extreme)
    simhours = (t[-1]-t[0]) / 3600
    # get the associated asymptotic gumbel params for the duration of interest
    n = (duration / simhours) * weib_qats.data.size
    gloc, gscale = weib_qats.gumbel_parameters(n) # maxima_space (correct space with gumbel_l)
    # convert to relevant scipy implements
    gumbel, weibull = gumbel_r, weibull_min
    weib = weibull(loc=loc, scale=scale, c=shape) # Distribution of population extremes
    evd = gumbel(loc=gloc, scale=gscale)  # Extreme Value Distribution
    # Compute statistics (working with maxima)
    evd_mpm = gloc
    evd_mean = gloc + sign*gscale*0.5772156649
    evd_90 = evd.ppf(0.9)    
    # make plots
    fig, ax1 = plt.subplots() # make axes
    yspace = lambda probability:  np.log(-np.log(1-probability))
    xspace = lambda xvalue: np.log(abs(xvalue-loc))
    # Add data points
    F_p, x_p = empirical_cdf(len(x[ix])), np.sort(x[ix])  # data points
    ax1.plot(xspace(x_p), yspace(F_p), color='r', linewidth=2, label="Empirical (data)")
    # Add weibull fit to plot
    x_fit = np.linspace(weib.ppf(0.01), weib.ppf(0.9999), 100) # x-range of interest for labelling
    F_fit = weib.cdf(x_fit)
    ax1.plot(xspace(x_fit),yspace(F_fit), color='k', label="Weibull fit")
    # Set yticks and labels
    yticklabels = np.r_[0.1, 0.2, 0.5, 0.7, 0.9, 0.99, 0.999, 0.9999]
    yticks = yspace(yticklabels)
    ax1.set_yticks(yticks)    
    ax1.set_yticklabels(yticklabels)    
    # Set xticks and labels
    xticklabels = weib.ppf(yticklabels)
    xticks = xspace(xticklabels)
    ax1.set_xticks(xticks)    
    ax1.set_xticklabels("%.1f" % (sign*l) for l in xticklabels)    
    ax1.grid(True)
    ax1.set_xlim(xticks[0], xticks[-1])
    ax1.set_ylim(yticks[0], yticks[-1])
    # Plot the most probable extreme for the duration from the weibull
    p = 1 / weib_qats.data.size * simhours / duration   
    #p = 1 - p if not maxima else p
    ax1.scatter([xspace(x_p[-1])], [yspace(F_p[-1])], color='r', marker='o', label=f"Sample extr ({sign*x_p[-1]:.1f})")
    ax1.scatter([xspace(weib.ppf(1-p))], [yspace(1-p)], color='k', marker='o', label=f"Weibull est. extr ({sign*weib.ppf(1-p):.1f})")
    ax1.legend(loc=0)
    if savefig:
        plt.savefig(figname)    
        return (sign*x_p[-1], sign*weib.ppf(1-p), sign*evd_mpm, sign*evd_mean, sign*evd_90)
    else:
        return (sign*x_p[-1], sign*weib.ppf(1-p), sign*evd_mpm, sign*evd_mean, sign*evd_90), ax1