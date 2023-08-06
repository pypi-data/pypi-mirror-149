#!/home/draugen/a/tken/Python254/bin/python

#
# Usage: General postprocessing tool for WAMIT.out file(s)
#

# Read in modules
import optparse
import sys
import os
from numpy import array, zeros, eye, e, pi, all, ones
import matplotlib.ticker as ticker
from pylab import *
from ..administration.tools import runprocess, multipleReplace, find_occurrences

import subprocess as sp
from datetime import date

class Usage(Exception):
    """ Standard Error Handler """
    def __init__(self, msg):
        self.msg = msg

#
# Helper functions and class
#

def phase0(ph, mode):
    """ With symmetries X = 0 and Y = 0 apply phase transformation
    
           Wdir:  0
           Surge: 0.  Sway:  0.  Heave: 0.
           Roll:  pi  Pitch: pi  Yaw:   pi

    This is a combination of 2 transformations:

    1. Wamit 0->90 to Wamit 90->180
 
            Wdir:  180-theta
            Surge: pi  Sway:  0.  Heave: 0.
            Roll:  0.  Pitch: pi  Yaw:   pi

    2. Wamit (90->180) to Mossi (0->90)

            Wdir:  180-theta
            Surge: pi  Sway:  0.  Heave: 0.
            Roll:  pi  Pitch: 0.  Yaw:   0.
           
    N.B. The latter transformation is opposite to that
    given in RIFLEX-C appendix 7A and WAMOF theory manuals.
    However it is specified as above in the WAM2MOS manual
    written by Knut Mo. The RIFLEX and WAMOF manuals appear
    to have a phase shift of pi for all modes. Having spoken
    Knut the reason for the extra pi shift in WAM2MOS
    is because the wave has a phase shift of pi. 

    Therefore all transfer functions have a phase shift of pi. 
    The WAMOF code has a slightly quirkier specification than
    WAMIT, however I found that the asymptotic limit of WAMIT
    and WAMOF were the same :/. Anyway I am happy with Knuts 
    logic! Further I have checked that his code exports as 
    above. 
    
    It also seems that the wave drift are opposite to that
    above :/ This is possibly due to an extra pi change as
    the wave drift has 2 waves hence pi of the second needs
    considering. :/ not sure on this logic. 
    """
    
    Surge, Sway, Heave, Roll, Pitch, Yaw = 0, 1, 2, 3, 4, 5
    if mode == Surge: phase = ph + 0.
    if mode == Sway:  phase = ph + 0.
    if mode == Heave: phase = ph + 0.
    if mode == Roll:  phase = ph + 180.
    if mode == Pitch: phase = ph + 180.
    if mode == Yaw:   phase = ph + 180.  
    if phase > 360.: phase = phase - 360.
    return phase

def phase1(ph, mode):
    """ 
        With only Y=0 plane symmetry or no-symmetry apply phase transformation
        
            Wdir:  180-theta
            Surge: pi  Sway:  0.  Heave: 0.
            Roll:  pi  Pitch: 0.  Yaw:   0. """
    Surge, Sway, Heave, Roll, Pitch, Yaw = 0, 1, 2, 3, 4, 5      
    if mode == Surge: phase = ph + 180.
    if mode == Sway:  phase = ph + 0.
    if mode == Heave: phase = ph + 0.
    if mode == Roll:  phase = ph + 180.
    if mode == Pitch: phase = ph + 0.
    if mode == Yaw:   phase = ph + 0.        
    if phase > 360.: phase = phase - 360.
    return phase

def dirch0(d):
    return d
    
def dirch1(d):
    d2 = 180. - d 
    if d2 > 360.: d2 = d2 - 360.
    return d2

def pha(z):
    return math.atan2(z.imag,z.real)*180./math.pi

                
def find_locations(string,data):
    return [loc for loc, line in enumerate(data) if string in line]


def flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in flatten(e):
        yield f
    else:
      yield e



def main():
    """ Main program for wamitlib.py """
    parser = optparse.OptionParser(
             description= 'General postprocessor for mimosa',
             prog       = 'mimosa.py',
             version    = 'mimosa.py 0.1',
             usage      = '%prog [options]')

    # define options
    parser.add_option('-w', dest="wamitfile", help="Wamit to Mossi Conversion")
    parser.add_option('-a', dest="amplitude", help="Incl. WAMOF heave (req. files must exist!)")
    parser.add_option('-c', action="store_true", help="Compare <mosfile 1> <mosfile 2>")
    parser.add_option('-s', dest="skiplist",  help="Smooth over id list of bad WD Coeffs")    

    options, arguments = parser.parse_args()

    # MENU MENU MENU MENU MENU MENU :) :/ 8(
    if options.wamitfile is not None: 
        return(wam2mos(options.wamitfile,options.amplitude,options.skiplist))
    if (options.c) and len(arguments) is not 2: 
        print("Need 2 arguments for this option: %d provided" % len(arguments))
        print(parser.print_help()); return
    if (options.c): return(compare_mossies(arguments))

    print(parser.print_help()); return
    

def wam2mos(wamitfile, amplitude, skiplist):
    """ Converts wamit files to mossi files """
    if amplitude is not None:
        data = None #read_wamit2(wamitfile,amplitude,skiplist)
    else:
        data = None #read_wamit(wamitfile, skiplist)
    # Open the Mossi FILE
    mossi = open(wamitfile.strip(".out") + (".mos"),"w")
    mossi.write("'File Generated using wam2mos.py'\n")
    mossi.write("'WAMIT FILE: %s, Date: %s, User ID: TEK'\n" % (wamitfile,date.today().isoformat()))
    # Output DATA Group 1
    mossi.write("'DATA GROUP 1 - MASS, ADDED MASS AND HYDRODYNAMIC STIFFNESS'\n")
    mossi.write("11000 Dry Mass Matrix\n")
    mossi.write("11100 0.0 0.0 0.0\n")    
    # Output Mass Matrix
    M = data["Mass"]
    M[4,0] = -M[4,0]; M[0,4] = -M[0,4]
    M[3,1] = -M[3,1]; M[1,3] = -M[1,3] 
    M[3,2] = -M[3,2]; M[2,3] = -M[2,3] 
    M[5,0] = -M[5,0]; M[0,5] = -M[0,5] 
    M[3,4] = -M[3,4]; M[4,3] = -M[4,3] 
    M[5,3] = -M[5,3]; M[3,5] = -M[3,5]
    #if M.all() == 0. : print "Mass matrix not found"
    for i in range(0,6): mossi.write("1110%d%12.4e%12.4e%12.4e%12.4e%12.4e%12.4e\n" 
              % (i+1, M[i,0], M[i,1], M[i,2], M[i,3], M[i,4], M[i,5]))
    # Output Added Mass Data
    A = data["AddedMass"]; T     = data["Periods"]
    mossi.write("11200 Added Mass Matrix (at T = %.1f secs)\n" % max(T))
    AM = A[T.argmax(),:,:]
    AM[4,0] = -AM[4,0]; AM[0,4] = -AM[0,4]
    AM[3,1] = -AM[3,1]; AM[1,3] = -AM[1,3] 
    AM[0,2] = -AM[0,2]; AM[2,0] = -AM[2,0] 
    AM[3,2] = -AM[3,2]; AM[2,3] = -AM[2,3] 
    AM[5,0] = -AM[5,0]; AM[0,5] = -AM[0,5] 
    AM[3,4] = -AM[3,4]; AM[4,3] = -AM[4,3] 
    AM[5,3] = -AM[5,3]; AM[3,5] = -AM[3,5]
    for i in range(0,6): mossi.write("1120%d%12.4e%12.4e%12.4e%12.4e%12.4e%12.4e\n" 
              % (i+1, AM[i,0], AM[i,1], AM[i,2], AM[i,3], AM[i,4], AM[i,5]))
    # Output Gravitational and Hydrostatic Stiffness Matrix
    K = data["KMatrix"]
    mossi.write("12000 Hydrostatic Stiffness Data\n")
    mossi.write("12100%12.1f%12.1f\n" % (0., 0.))    
    mossi.write("12101%12.3e%12.3e%12.3e\n" % (K[2,2],K[2,3],K[2,4]))
    mossi.write("12102%12.3e%12.3e%12.3e\n" % (K[3,2],K[3,3],K[3,4]))
    mossi.write("12103%12.3e%12.3e%12.3e\n" % (K[4,2],K[4,3],K[4,4]))
    # Output Wind and Current Coefficients
    mossi.write("'DATA GROUP 2 - CURRENT AND WIND FORCE COEFFICIENTS'\n")
    mossi.write("20000 Coefficients from Wind Tunnel Tests\n")
    mossi.write("'Quadratic and Linear Current Coefficients'\n")
    #mossi.write("'# of Quadratic and Linear Current Coefficients\n")
    mossi.write("23100  37 37\n")
    #mossi.write("'Quadratic Current Coefficients\n")
    for i in range(0,37):
        mossi.write("231%02d%12.1f%12.3e%12.3e%12.3e%12.3e%12.3e%12.3e\n" % \
                            (i+1, i*10., 0., 0., 0., 0., 0., 0.))
    #mossi.write("'Linear Current Coefficients\n")
    for i in range(0,37):
        mossi.write("232%02d%12.1f%12.3e%12.3e%12.3e%12.3e%12.3e%12.3e\n" % \
                            (i+1, i*10., 0., 0., 0., 0., 0., 0.))
    # Output Quadratic Damping Force
    mossi.write("'Quadratic Damping Coefficients'\n")
    mossi.write("23500 0.0 0.0 \n")
    for i in range(1,7):
        mossi.write("2350%d%12.3e\n" % (i,0.))
                
    mossi.write("'Linear Damping Coefficients'\n")
    mossi.write("23600 0.0 0.0 \n")
    for i in range(1,7):
        mossi.write("2360%d%12.3e%12.3e%12.3e%12.3e%12.3e%12.3e\n" % \
                            (i, 0., 0., 0., 0., 0., 0.))              
    # Output Wind force coefficients
    mossi.write("'Quadratic Wind Force Coefficients'\n")
    #mossi.write("'# of Wind Force Coefficients\n")
    mossi.write("24100  37\n")
    for i in range(0,37):
        mossi.write("241%02d%12.1f%12.3e%12.3e%12.3e%12.3e%12.3e%12.3e\n" % \
                            (i+1, i*10., 0., 0., 0., 0., 0., 0.))
    # Need to sort frequencies into ascending order
    T     = data["Periods"]; w   = 2*pi/T; Dir = data["Headings"]
    Drift = data["Drift_P"]; RAO = data["R.A.O"]; 

    # temporarily replace Drift_P with Drift_M for surge direction!
    #Drift2 = data["Drift_M"]; Drift[:,:,0] = Drift2[:,:,0]*1.0
    
    # temporarily scale surge drift by 15%
    #Drift[:,:,0] = Drift[:,:,0]*1.15

    sym = data["Symmetry"];  wavek = data["Wavenumbers"]
    if (w[0] > w[1]): 
        w = w[::-1] # Reverse frequencies and reverse array rows
        wavek = wavek[::-1] # Reverse wave numbers
        for m in range(0,6): # Note numpy arrays are referenced
            Drift[:,:,m] = Drift[::-1,:,m].copy() #could use *1
            RAO[:,:,m]   = RAO[::-1,:,m].copy()   #could use *1
    # Need drift coefficients at least between (0,180)    
    if sym =="X&Y":
        Dir2   = zeros(2*len(Dir)-1) #-1 as they share 90
        Drift2 = zeros((len(w),len(Dir2),6))
        for i, d in enumerate(Dir):
            Dir2[i]  = d; Dir2[-(i+1)] = 180.-d
        for i, f in enumerate(w):
            for j, d in enumerate(Dir):
                for m in range(0,6):
                    Drift2[i,  j   ,m] = Drift[i,j,m]
                    Drift2[i,-(j+1),m] = Drift[i,j,m]
                    # Need a pi change for Surge, Pitch and Yaw
                    if m == 0 or m > 3: Drift2[i,-(j+1),m] = -Drift[i,j,m]
    # Set transformations for mossiconversion
    dirchange   = {0 : dirch0, 1 : dirch1}
    phasechange = {0 : phase0, 1 : phase1}
    print("%s symmetry plane(s) found" % sym)
    if sym == "X&Y": itrans = 0; isys = 2
    if sym == "Y=0": itrans = 1; isys = 1
    if sym == None:  itrans = 1; isys = 0
    if sym == "X=0":
        print("Not implemented")
        sys.exit(-1)
    mossi.write("'DATA GROUP 3 - TRANSFER FUNCTION COEFFICIENTS'\n")                
    mossi.write("30000 Motion Transfer Functions\n")                
    mossi.write("30100 %d" % len(w))
    # Output Frequencies
    j = 1 
    for i, f in enumerate(w):
        if i % 5 == 0:
            mossi.write("\n301%02d" % j)
            j = j + 1
        mossi.write("%12.4f" % f)
        if (i+1) == len(w):
            mossi.write("\n")
    # Output directions
    if sym == "X&Y": ind = list(range(0,len(Dir)))
    else:            ind = list(range(len(Dir)-1,-1,-1))
    j = 1 
    if Dir[0] > Dir[1]: print("Wamit directions descending :/")
    mossi.write("30200 %d %d" % (len(Dir), isys))
    for k, i in enumerate(ind): 
        if k % 5 == 0:
            mossi.write("\n302%02d" % j)
            j = j + 1
        mossi.write("%12.1f" % (dirchange[itrans](Dir[i])))
        if (k+1) == len(Dir):
            if k % 5 is not 0:
                mossi.write("\n")
    # Output Water Depth
    mossi.write("30300 %s\n" % data["Depth"])
    # R.A.Os
    k = 30
    for d in ind:
        k = k + 1
        if k == 40: k = 31
        for m, mode in enumerate(["Surge","Sway","Heave"]):
            for i in range(0,len(w)):
                mossi.write("%02d%d%02d%12.3e%12.3e\n" % 
                                (k, m+1, i+1, abs(RAO[i,d,m]), 
                                 phasechange[itrans](pha(RAO[i,d,m]),m)))
                    
        for n, mode in enumerate(["Roll","Pitch","Yaw"]):
            m = n + 3
            for i in range(0,len(w)):
                mossi.write("%02d%d%02d%12.3e%12.3e\n" % 
                                (k, m+1, i+1, abs(RAO[i,d,m])/wavek[i], 
                                 phasechange[itrans](pha(RAO[i,d,m]),m)))


    # Output Wave drift
    if sym == "X&Y":
        Dir = Dir2; Drift = Drift2
    mossi.write("'DATA GROUP 4 - WAVE DRIFT FORCE COEFFICIENTS'\n")
    mossi.write("40000 Mean Wave Drift Coefficients (no scaling)\n")
    mossi.write("40100 %d %d Aranha 50." % (len(w),len(Dir)))
    # Output frequencies
    k = 1
    for i, f in enumerate(w):
        if i % 5 == 0:
            mossi.write("\n402%02d" % k)
            k = k + 1
        mossi.write("%12.4f" % f)     
    # directions (note that for wave drift, the X&Y=0 case
    # has been expanded to a Y=0 case, hence Dir[::-1].
    # Also the itrans and isym need changing to Y=0 case
    if sym == "X&Y": itrans = 1; isys = 1
    k = 1
    for i, d in enumerate(Dir[::-1]):
        if i % 5 == 0:
            mossi.write("\n403%02d" % k)
            k = k + 1
        mossi.write("%12.1f" % (dirchange[itrans](d)))
        if (i+1) == len(Dir):
            if i % 5 is not 0:
                mossi.write("\n")
    # W.D. Coefficients
    k = 0
    for d in range(len(Dir)-1,-1,-1):
        k = k + 1
        if k == 10: k = 1
        for i in range(0,len(w)):
            p0 = pha(Drift[i,d,0])
            p1 = pha(Drift[i,d,1])
            p2 = pha(Drift[i,d,2])
            p3 = pha(Drift[i,d,3])
            p4 = pha(Drift[i,d,4])
            p5 = pha(Drift[i,d,5])
            sign = [1,1,1,1,1,1]
            # apply an implicit pi phase shift (as wave cancels)
            for m, p in enumerate([p0,p1,p2,p3,p4,p5]):
                #if 170. < abs(phasechange[itrans](p,m)) < 190.: 
                if  abs(phasechange[itrans](p,m))> 340. or \
                        abs(phasechange[itrans](p,m))<  20.: 
                    sign[m] = -1
                #
            mossi.write("41%d%02d" % (k, i+1)) 
            mossi.write("%12.3e%12.3e%12.3e%12.3e%12.3e%12.3e\n" % 
                        (abs(Drift[i,d,0])*sign[0],
                         abs(Drift[i,d,1])*sign[1],
                         abs(Drift[i,d,2])*sign[2],
                         abs(Drift[i,d,3])*sign[3],
                         abs(Drift[i,d,4])*sign[4],
                         abs(Drift[i,d,5])*sign[5]))

def find_mossi_id(data,id):
    for l, line in enumerate(data):
        if line.startswith(id): return l
    return None

def read_mossi(mos):
    print("Scanning %s" % mos)
    data = open(mos, "r").readlines()
    loc  = find_mossi_id(data,"40100")
    id, nf, nd = [float(i) for i in data[loc].strip().split()[:3]]
    nf, nd, cl = int(nf), int(nd), loc + 1
    nflines, ndlines = (nf-1) / 5 + 1, (nd-1)/5 + 1
    freqblock = data[cl:cl+nflines]
    headblock = data[cl+nflines:cl+nflines+ndlines]
    L = [line.split()[1:] for line in freqblock]
    freqs = array([float(i) for i in list(flatten(L))])
    L = [line.split()[1:] for line in headblock]
    heads = array([float(i) for i in list(flatten(L))])
    cl = cl+nflines+ndlines; DOF = len(data[cl].strip().split()[1:])
    print("Reading %d-DOF Wave Drift Coefficients" % DOF) 
    L = [line.split()[1:] for line in data[cl:cl+nf*nd]]
    WDCoeffs = array([float(i) for i in list(flatten(L))]).reshape((nd,nf,DOF))
    return {"Frequencies": freqs, "Headings": heads, "WDCoeffs": WDCoeffs, "DOF": DOF}


def compare_mossies(mossifiles):
    mos1, mos2 = mossifiles
    VD1 = read_mossi(mos1)
    VD2 = read_mossi(mos2)
    h1, f1, wd1 = VD1["Headings"], VD1["Frequencies"], VD1["WDCoeffs"]
    h2, f2, wd2 = VD2["Headings"], VD2["Frequencies"], VD2["WDCoeffs"]
    figure(figsize=(11,6))
    axes([0.15,0.1,0.65,0.75])
    ax = gca()
    ax.semilogx()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.f"))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    #ax.set_xticks([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70])
    ax.set_xticks([2,3,4,5,6,7,8,9,10,20,30,40,50,60,70])
    ax.xaxis.grid(True, which='minor')
    ax.xaxis.grid(True, which='major', color='k', linestyle='--')
    ax.yaxis.grid(True, which='major')
    title("Mean Drift Force Coefficient in Surge")# + mode) 
    plot(2*pi/f2,wd2[0,:,0],marker="D")
    plot(2*pi/f1,wd1[0,:,0],marker="^")
    grid(True)
    xlabel("Period [s]")
    #ylabel(ftype[m][1] + 
    #       " / Amplitude Squared of Incident Wave kN/m^2")# + ftype[m][0])
    #xlim(0.,xmax)
    T1, T2 = 2*pi/f1, 2*pi/f2
    xlim(2.,1.5*2*pi/f2[0])
    ind = nonzero(T2>=2)[0]
    #ylim(1.5*(wd1[ix_(ind),:,m].real).min()/1000.,
    #     1.5*(wd2[ix_(ind),:,m].real).max()/1000.)
    #savefig("figures/"+dt[1]+"_"+mode+".png")
    #savefig("figures/"+dt[1]+"_"+mode+".eps")
    show()


#
#---- EXPORT REPORT FILE FOR POSITIONING SYSTEM
#


POSITIONINGMACRO = \
""" /            ' Long-term simulation ? (N)
 @ wait off
 3               ' Number of degrees of freedom (3 or 6)
 REPORT.DAT
 /               ' Append data to file if it already exists ? (N)
 Output positioning system
 for conversion to riflex inpmod
 READ SYSTEM                   ' SYSTEM
 MOORING SYSTEM                ' SYSTEM READ
 xxxmim
 Return                        ' SYSTEM READ
   MOORING SYSTEM COMPUTATION  ' SYSTEM
 /                     ' Result to file ? (N)
   SYSTEM                      ' MOORING SYSTEM COMPUTATIONS
 PRINT/DRAW/STORE SYSTEM       ' SYSTEM
 POSITIONING SYSTEM PRINTOUT   ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 y                     ' Results to file ? (N)
 LINE CHARACTERISTICS PRINTOUT ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 y                     ' Results to file ? (N)
 Return                        ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 Terminate                     ' SYSTEM
"""

def returnpositioningdata(mimfile):
    """ Returns tuple (linedata, linecharacteristics)
          
           linedata is a dictionary of linedata :)

           linecharacteristics is a list containing:

               1. dictionarys where the line characteristic is used
               2. or the following strings
                     'Line characteristic not used (removed)'
                     'Table is direct input'

    """

    # RUN MIMOSA AND EXPORT A REPORT FILE
    #-----------------------------------------
    MACRO = multipleReplace(POSITIONINGMACRO, 
                            {'xxxmim':mimfile}) 
    with open('MIMOSA.INP','w') as macroFile:
        macroFile.write(MACRO)
    #runprocess("C:/Appl/BatchScripts/mimosa.bat") # generates REPORT file
    os.system("C:/Appl/BatchScripts/mimosa.bat") # generates REPORT file
    with open('REPORT.DAT','r') as repFile:
        reportlines = repFile.readlines()
    with open(mimfile, 'r') as mimFile: 
        mimlines    = mimFile.readlines()
    numberofmooringlines = len(find_occurrences('LINE DATA', mimlines))
    # GET FAIRLEAD INFORMATION
    #-----------------------------------------
    skiplines = 7
    location = find_occurrences('LINE DATA', reportlines, 
                    specificOccurrenceWanted= 1) + skiplines
    informationonfairleads = reportlines[location:location+numberofmooringlines]
    xyfairlead = np.zeros((numberofmooringlines, 2))
    linechar   = np.zeros(numberofmooringlines,np.int)
    for i, line in enumerate(informationonfairleads): 
        words = line.split()
        xyfairlead[i,:] = np.r_[[float(word) for word in words[-2:]]]
        linechar[i] = int(words[1])

    #----------------------------------------------------------
    location = find_occurrences('Heading (rel. North)', reportlines,
                               specificOccurrenceWanted =1)
    vesselheading = reportlines[location].split(':')[1]
    vesselheading = float(vesselheading.strip().strip('deg.'))
    #----------------------------------------------------------
    location = find_occurrences('X1  (Northwards)', reportlines,
                               specificOccurrenceWanted =1)
    vesselxoffset = reportlines[location].split(':')[1]
    vesselxoffset = float(vesselxoffset.strip().strip('m'))
    #----------------------------------------------------------
    location = find_occurrences('X2  (Eastwards)', reportlines,
                               specificOccurrenceWanted =1)
    vesselyoffset = reportlines[location].split(':')[1]
    vesselyoffset = float(vesselyoffset.strip().strip('m'))
    

    
    # GET ANCHOR COORDINATES, TENSION ETC ...
    #-----------------------------------------
    skiplines = 6
    location = find_occurrences('LINE INITIALIZING DATA', reportlines, 
                               specificOccurrenceWanted = 1) + skiplines
    informationonanchor = reportlines[location:location+numberofmooringlines]
    xyanchor   = np.zeros((numberofmooringlines, 2))
    heading    = np.zeros(numberofmooringlines)
    tension    = np.zeros(numberofmooringlines)
    horizontal = np.zeros(numberofmooringlines)
    winchlength= np.zeros(numberofmooringlines)
    for i, line in enumerate(informationonanchor):
        words = line.replace('*)','').split()
        xyanchor[i,:] = np.r_[[float(word) for word in words[-3:-1]]]
        heading[i], tension[i], horizontal[i] = \
            [float(word) for word in words[1:-3]]
        winchlength[i] = float(words[-1])

    # GET LINE CHARACTERISTICS (FROM MIM FILE)
    #-----------------------------------------
    locations = find_occurrences('LINE CHARACTERISTIC NUMBER', reportlines)
    numberoflinechar = len(locations)
    linecharacteristics = [None]*numberoflinechar
    locations.append(len(reportlines))
    for startloc, endloc in zip(locations[:-1],locations[1:]):
        ok = True
        linecharblockofdata = reportlines[startloc:endloc] 
        #---------------------------------------------------------------
        for line in linecharblockofdata:
            if 'LINE CHARACTERISTIC NUMBER' in line: 
                lchar = int(line.split(':')[1])
            if 'Table is direct input' in line: 
                linecharacteristics[lchar-1] = 'Table is direct input'
                ok = False
        if lchar not in linechar: 
            linecharacteristics[lchar-1] = 'Line characteristic not used (removed)'
            ok = False
        if not ok: continue # = cycle: poor terminology borrowed from C
        #---------------------------------------------------------------
        for line in linecharblockofdata:
            if 'LINE CHARACTERISTIC NUMBER' in line: 
                lchar = int(line.split(':')[1])
            if 'fairlead' in line: zfairlead = float(line.split(':')[1])
            if 'anchor'   in line: zanchor   = float(line.split(':')[1])
            if 'segments' in line: nsegments = int(line.split(':')[1])
        #---------------------------------------------------------------
        skiplines = 1
        location  = find_occurrences('elements', linecharblockofdata,
                                    specificOccurrenceWanted = 1) + skiplines
        subblock = linecharblockofdata[location:location+nsegments]
        nelseg   = np.zeros(nsegments, int)
        ibuoy    = np.zeros(nsegments, int)
        slength  = np.zeros(nsegments)        
        for i, line in enumerate(subblock): 
            words = line.split()
            nelseg[i], ibuoy[i] = int(words[2]), int(words[3])
            slength[i] = float(words[4]) 
        #---------------------------------------------------------------
        skiplines = 2
        location  = find_occurrences('elasticity', linecharblockofdata,
                                    specificOccurrenceWanted = 1) + skiplines
        subblock = linecharblockofdata[location:location+nsegments]
        diameter, emod, emfact, uwiw, watfac, cdn, cdl = \
            [np.zeros(nsegments) for i in range(0,7)]
        for i, line in enumerate(subblock):
            diameter[i], emod[i], emfact[i], uwiw[i], \
                watfac[i], cdn[i], cdl[i] = \
                [float(word) for word in line.split()[1:]]
        #---------------------------------------------------------------
        # pack into a dictionary 
        linecharacteristics[lchar-1] = \
            {'lchar'    : lchar,
             'nelseg'   : nelseg,
             'zfairlead': zfairlead,
             'zanchor'  : zanchor,
             'nsegments': nsegments,
             'slength'  : slength,
             'ibuoy'    : ibuoy,
             'slength'  : slength,
             'diameter' : diameter,
             'emod'     : emod,
             'emfact'   : emfact,
             'uwiw'     : uwiw,
             'watfac'   : watfac,
             'cdn'      : cdn,
             'cdl'      : cdl}
    
    #---------------------------------------------------------------
    linedata = \
        {'linechar'   : linechar,
         'xyfairlead' : xyfairlead,
         'xyanchor'   : xyanchor, 
         'heading'    : heading, 
         'tension'    : tension, 
         'horizontal' : horizontal,
         'winchlength': winchlength,
         'vesselheading': vesselheading,
         'vesselxoffset': vesselxoffset,
         'vesselyoffset': vesselyoffset}

    # GET BUOY DATA
    #-----------------------------------------
    locations = find_occurrences('ZBUOY (m)', reportlines)
    numberofbuoys = len(locations)
    buoyinfo      = [None]*numberofbuoys
    for i, loc in enumerate(locations): 
        zbuoy, fbuoy = reportlines[loc+1].split()
        buoyinfo[i] = (float(zbuoy), float(fbuoy))
    #---------------------------------------------------------------
    return (linedata, linecharacteristics, buoyinfo)


#-----------------------------------------------------------

POSITIONINGMACRO2 = \
""" /            ' Long-term simulation ? (N)
 @ wait off
 3               ' Number of degrees of freedom (3 or 6)
 REPORT.DAT
 /               ' Append data to file if it already exists ? (N)
 Output positioning system
 for conversion to riflex inpmod
 READ SYSTEM                   ' SYSTEM
 MOORING SYSTEM                ' SYSTEM READ
 xxxmim
 Return                        ' SYSTEM READ
   MOORING SYSTEM COMPUTATION  ' SYSTEM
 /                     ' Result to file ? (N)
 EQUILIBRIUM POSITION          ' MOORING SYSTEM COMPUTATIONS
 y                     ' Move vessel to equilibrium position? (Y)
 n                     ' Results to file ? (N)
 n                     ' Result to file ? (N)
   SYSTEM                      ' MOORING SYSTEM COMPUTATIONS
 PRINT/DRAW/STORE SYSTEM       ' SYSTEM
 POSITIONING SYSTEM PRINTOUT   ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 y                     ' Results to file ? (N)
 LINE CHARACTERISTICS PRINTOUT ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 y                     ' Results to file ? (N)
 Return                        ' PRINT/DRAW/STORE POSITIONING SYSTEM DATA
 Terminate                     ' SYSTEM
"""



def returnpositioningdata2(mimfile):
    """ Returns tuple (linedata, linecharacteristics)
          
           linedata is a dictionary of linedata :)

           linecharacteristics is a list containing:

               1. dictionarys where the line characteristic is used
               2. or the following strings
                     'Line characteristic not used (removed)'
                     'Table is direct input'

    """

    # RUN MIMOSA AND EXPORT A REPORT FILE
    #-----------------------------------------
    MACRO = multipleReplace(POSITIONINGMACRO2, 
                            {'xxxmim':mimfile}) 
    open('RUN.MAC','w').write(MACRO)
    runprocess("mimosa < RUN.MAC") # generates REPORT file
    reportlines = open('REPORT.DAT','r').readlines()
    mimlines    = open(mimfile, 'r').readlines()
    numberofmooringlines = len(find_occurrences('LINE DATA', mimlines))

    # GET FAIRLEAD INFORMATION
    #-----------------------------------------
    skiplines = 7
    location = find_occurrences('LINE DATA', reportlines, 
                                specificOccurrenceWanted = 1) + skiplines
    informationonfairleads = reportlines[location:location+numberofmooringlines]
    xyfairlead = np.zeros((numberofmooringlines, 2))
    linechar   = np.zeros(numberofmooringlines,np.int)
    for i, line in enumerate(informationonfairleads): 
        words = line.split()
        xyfairlead[i,:] = np.r_[[float(word) for word in words[-2:]]]
        linechar[i] = int(words[1])

    #----------------------------------------------------------
    location = find_occurrences('Heading (rel. North)', reportlines,
                               specificOccurrenceWanted =1)
    vesselheading = reportlines[location].split(':')[1]
    vesselheading = float(vesselheading.strip().strip('deg.'))
    #----------------------------------------------------------
    location = find_occurrences('X1  (Northwards)', reportlines,
                               specificOccurrenceWanted =1)
    vesselxoffset = reportlines[location].split(':')[1]
    vesselxoffset = float(vesselxoffset.strip().strip('m'))
    #----------------------------------------------------------
    location = find_occurrences('X2  (Eastwards)', reportlines,
                               specificOccurrenceWanted =1)
    vesselyoffset = reportlines[location].split(':')[1]
    vesselyoffset = float(vesselyoffset.strip().strip('m'))
    

    
    # GET ANCHOR COORDINATES, TENSION ETC ...
    #-----------------------------------------
    skiplines = 6
    location = find_occurrences('LINE INITIALIZING DATA', reportlines, 
                               specificOccurrenceWanted = 1) + skiplines
    informationonanchor = reportlines[location:location+numberofmooringlines]
    xyanchor   = np.zeros((numberofmooringlines, 2))
    heading    = np.zeros(numberofmooringlines)
    tension    = np.zeros(numberofmooringlines)
    horizontal = np.zeros(numberofmooringlines)
    winchlength= np.zeros(numberofmooringlines)
    for i, line in enumerate(informationonanchor):
        words = line.replace('*)','').split()
        xyanchor[i,:] = np.r_[[float(word) for word in words[-3:-1]]]
        heading[i], tension[i], horizontal[i] = \
            [float(word) for word in words[1:-3]]
        winchlength[i] = float(words[-1])

    # GET LINE CHARACTERISTICS (FROM MIM FILE)
    #-----------------------------------------
    locations = find_occurrences('LINE CHARACTERISTIC NUMBER', reportlines)
    numberoflinechar = len(locations)
    linecharacteristics = [None]*numberoflinechar
    locations.append(len(reportlines))
    for startloc, endloc in zip(locations[:-1],locations[1:]):
        ok = True
        linecharblockofdata = reportlines[startloc:endloc] 
        #---------------------------------------------------------------
        for line in linecharblockofdata:
            if 'LINE CHARACTERISTIC NUMBER' in line: 
                lchar = int(line.split(':')[1])
            if 'Table is direct input' in line: 
                linecharacteristics[lchar-1] = 'Table is direct input'
                ok = False
        if lchar not in linechar: 
            linecharacteristics[lchar-1] = 'Line characteristic not used (removed)'
            ok = False
        if not ok: continue # = cycle: poor terminology borrowed from C
        #---------------------------------------------------------------
        for line in linecharblockofdata:
            if 'LINE CHARACTERISTIC NUMBER' in line: 
                lchar = int(line.split(':')[1])
            if 'fairlead' in line: zfairlead = float(line.split(':')[1])
            if 'anchor'   in line: zanchor   = float(line.split(':')[1])
            if 'segments' in line: nsegments = int(line.split(':')[1])
        #---------------------------------------------------------------
        skiplines = 1
        location  = find_occurrences('elements', linecharblockofdata,
                                    specificOccurrenceWanted = 1) + skiplines
        subblock = linecharblockofdata[location:location+nsegments]
        nelseg   = np.zeros(nsegments, int)
        ibuoy    = np.zeros(nsegments, int)
        slength  = np.zeros(nsegments)        
        for i, line in enumerate(subblock): 
            words = line.split()
            nelseg[i], ibuoy[i] = int(words[2]), int(words[3])
            slength[i] = float(words[4]) 
        #---------------------------------------------------------------
        skiplines = 2
        location  = find_occurrences('elasticity', linecharblockofdata,
                                    specificOccurrenceWanted = 1) + skiplines
        subblock = linecharblockofdata[location:location+nsegments]
        diameter, emod, emfact, uwiw, watfac, cdn, cdl = \
            [np.zeros(nsegments) for i in range(0,7)]
        for i, line in enumerate(subblock):
            diameter[i], emod[i], emfact[i], uwiw[i], \
                watfac[i], cdn[i], cdl[i] = \
                [float(word) for word in line.split()[1:]]
        #---------------------------------------------------------------
        # pack into a dictionary 
        linecharacteristics[lchar-1] = \
            {'lchar'    : lchar,
             'nelseg'   : nelseg,
             'zfairlead': zfairlead,
             'zanchor'  : zanchor,
             'nsegments': nsegments,
             'slength'  : slength,
             'ibuoy'    : ibuoy,
             'slength'  : slength,
             'diameter' : diameter,
             'emod'     : emod,
             'emfact'   : emfact,
             'uwiw'     : uwiw,
             'watfac'   : watfac,
             'cdn'      : cdn,
             'cdl'      : cdl}
    
    #---------------------------------------------------------------
    linedata = \
        {'linechar'   : linechar,
         'xyfairlead' : xyfairlead,
         'xyanchor'   : xyanchor, 
         'heading'    : heading, 
         'tension'    : tension, 
         'horizontal' : horizontal,
         'winchlength': winchlength,
         'vesselheading': vesselheading,
         'vesselxoffset': vesselxoffset,
         'vesselyoffset': vesselyoffset}

    # GET BUOY DATA
    #-----------------------------------------
    locations = find_occurrences('ZBUOY (m)', reportlines)
    numberofbuoys = len(locations)
    buoyinfo      = [None]*numberofbuoys
    for i, loc in enumerate(locations): 
        zbuoy, fbuoy = reportlines[loc+1].split()
        buoyinfo[i] = (float(zbuoy), float(fbuoy))
    #---------------------------------------------------------------
    return (linedata, linecharacteristics, buoyinfo)





if __name__ == '__main__':
    sys.exit(main())
