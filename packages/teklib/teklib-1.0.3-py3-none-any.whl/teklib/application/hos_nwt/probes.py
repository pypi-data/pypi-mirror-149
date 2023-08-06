import string
import numpy as np
import matplotlib.pyplot as plt

def floadtxt(filename, comments='#', skiprows=0):
    """ For reading Fortran column data with 'D' formatting
    """
    with open(filename, 'r') as fin:
        lines = [l for l in fin.readlines() if not l.strip().startswith(comments)][skiprows:]
        #lines = [l for l in lines if len(l.split())!=0]
        return np.array([list(map(float, l.replace('D', 'E').split())) for l in lines])

def read_probes(filename, skiprows=2, plotfile=None):
    """ 
    Reads a probe.dat file from HOS-NWT and returns the data
    Optionally plots to plotfile   
    """
    data = floadtxt(filename, skiprows=2).T
    time = data[0]
    probes = data[1:]
    fig, axs = plt.subplots(nrows=len(data)-1, ncols=1)
    nprobes = len(probes)
    if plotfile is not None:
        for i in range(nprobes):
            axs[i].plot(time, probes[i], label='P%d' % (i+1))
            axs[i].legend(loc=0)
            axs[i].set_ylabel('[m]')
            if i == nprobes - 1: axs[i].set_xlabel("time [s]")
        axs[0].set_title("Wave elevations - HOS-NWT Probes")
        plt.savefig(plotfile)
    return (time, probes)