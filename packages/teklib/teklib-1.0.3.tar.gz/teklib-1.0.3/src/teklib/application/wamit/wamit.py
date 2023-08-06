#!/home/draugen/a/tken/Python254/bin/python

#
# Usage: General postprocessing tool for WAMIT.out file(s)
#


# Read in modules
import optparse
import sys
import os
from numpy import array, zeros, eye, e, pi, all, ix_, nonzero, max, angle, loadtxt
import matplotlib.ticker as ticker
from pylab import *
from ...reporting.latex import beamer
import subprocess as sp
from matplotlib.lines import Line2D

class Usage(Exception):
    """ Standard Error Handler """
    def __init__(self, msg):
        self.msg = msg
        
class WavePeriodDataBlock():
    """ Helper class for sorting wamit data in several files """
    def __init__(self,data):
        try:
            self.period = float(data[0].split()[4])
            self.data = data
        except ValueError:
            raise Usage("Does this work")    
    def __cmp__(self,other):
        return cmp(self.period, other.period)
                
class WavePeriodHeader():
    """ Helper class for sorting wamit data in several files """
    def __init__(self,line):
        try:
            self.period = float(line.split()[0])
            self.line = line
        except ValueError:
            raise Usage("Does this work")    
    def __cmp__(self,other):
        return cmp(self.period, other.period)


def read_dir_group(T,Dir,GROUP,data,n):
    """ Very Simple Group Reader """
    if len(GROUP) == 0: return None
    gr = zeros((len(T),len(Dir),6), complex)
    gap = 4
    for ip, loc in enumerate(GROUP):
        id = 0
        for l, line in enumerate(data[loc:]):
            if 'Wave Heading' in line:
                for line in data[loc+l+gap:loc+l+gap+n]:
                    string = "(" + (',').join(line.split()[0:3]) + ")"
                    k, mod, pha = eval(string)
                    gr[ip,id,k-1] = mod*e**(1j*pha*pi/180.)
                id = id + 1
            if id == len(Dir): break
    return gr


def remove_waveduplicates(L):
    """ Deprecate with Sets """
    new_List = []
    id       = []
    for i, item in enumerate(L):
        if item.period in new_List: continue
        new_List.append(item.period)
        id.append(i)
    return [L[i] for i in id]
        
def find_locations(string,data):
    return [loc for loc, line in enumerate(data) if string in line]


def main():
    """ Main program for wamitlib.py """
    parser = optparse.OptionParser(
             description= 'General postprocessor for wamit.out file(s)',
             prog       = 'wamit.py',
             version    = 'wamit.py 0.1',
             usage      = '%prog [options] wamitoutfile(s)')

    # define options
    parser.add_option('-o', dest="ofile", help="Amalgamates wamit files into OFILE")
    parser.add_option('-f', dest="ffile", help="Uses only frequencies in FFILE")
    parser.add_option('-d', dest="hfile", help="Uses only headings in HFILE")
    parser.add_option('-l', dest="pdflatex", help="Make report PDF")
    parser.add_option('-b', dest="pdfbeamer", help="Make slides PDF")
    parser.add_option('-p', action="store_true", help="Makes plots")
    parser.add_option('-s', dest="skiplist", help="Smooth over id list of bad WD Coeffs")    
    parser.add_option('-n', dest="name", default="", help="System identifier for plots")
    #parser.add_option('-t', dest="draft", default="", help="Draft  identifier for plots")
    
    options, arguments = parser.parse_args()

    if len(arguments) < 1: 
        print(parser.print_help())
        return -1

    # MENU MENU MENU MENU MENU MENU :) :/ 8(
    if options.ofile     is not None: return(amalg_wamit(options,arguments))
    if options.pdfbeamer is not None or \
       options.pdflatex  is not None or \
       options.p is True: plot_wamit(options,arguments)
    if options.pdflatex  is not None: return(exportlatex(options,arguments))
    if options.pdfbeamer is not None: return(exportbeamer(options,arguments))


def read_wamit(filename, skiplist = None):
    """ Returns a dictionary of Hydrodynamic Vessel Data read from WAMIT """

    print("Opening %s\n" % filename)
    wamitdata = open(filename, "r").readlines()
            
    # Get locations of various strings in the wamitdata
    Periods = find_locations("Wave period", wamitdata)
    Wavenum = find_locations("Wavenumber",  wamitdata)
    Heading = find_locations("Wave Heading",wamitdata)
    Gravity = find_locations("Gravity",     wamitdata)
    Length  = find_locations("Length",      wamitdata)
    Depth   = find_locations("depth",       wamitdata)
    Density = find_locations("density",     wamitdata)
    panels  = find_locations("panels",      wamitdata)
    SymXY   = find_locations("Symmetr",     wamitdata)
    XBODY   = find_locations("XBODY",       wamitdata)
    Volumes = find_locations("Volumes",     wamitdata)
    CB      = find_locations("Center of Buoyancy",     wamitdata)
    H20Grav = find_locations("restoring coefficients", wamitdata)
    CG      = find_locations("Center of Gravity",      wamitdata)
    Mass    = find_locations("mass matrix",            wamitdata)
    Damping = find_locations("damping matrix",         wamitdata)
    Stiff   = find_locations("stiffness matrix",       wamitdata)
    ADDEDMA = find_locations("ADDED-MASS AND DAMPING COEFFICIENTS",    wamitdata)
    HASKIND = find_locations("HASKIND EXCITING FORCES AND MOMENTS",    wamitdata) 
    DIFFRACT= find_locations("DIFFRACTION EXCITING FORCES AND MOMENTS",wamitdata) 
    RESPONSE= find_locations("RESPONSE AMPLITUDE OPERATORS",           wamitdata)
    DRIFTMOM= find_locations("DRIFT FORCES (Momentum Conservation)",   wamitdata)
    DRIFTPRE= find_locations("DRIFT FORCES (Pressure Integration)",    wamitdata)
            
    # Read periods, wavenumbers and compute radian wave frequencies
    T = array([float(wamitdata[loc].split()[4]) for loc in Periods])
    wavek = array([float(wamitdata[loc].split()[8]) for loc in Periods])
    w = 2 * pi / T
            
    # get wave headings (hidden bug that wamit.out has headings ascending)
    Dir = array([float(wamitdata[loc].split()[4]) for loc in Heading])
    Dir = sort(array(list(set(Dir)))) 
            
    # Quantities for dimensionalization 
    g   = 9.81; rho = 1025; sf = 1.0
    if float(wamitdata[Density[0]].split("density:")[1]) < 2.0: sf = 1000.
            
    # get mass matrix
    M = zeros((6,6))
    if len(Mass) > 0:
        loc = Mass[0]; 
        for i, line in enumerate(wamitdata[loc+1:loc+7]):
            M[i,:] = [float(j) for j in line.split()]
        M = M * sf
        #set_printoptions(precision=2)#; print M 
    # get hydrostatic and gravitational restoring coefficients
    loc = H20Grav[0]; C = zeros((6,6))
    C[2,2:5] = [float(cij) for cij in wamitdata[loc+1].split(':')[1].split()]
    C[3,3:6] = [float(cij) for cij in wamitdata[loc+2].split(':')[1].split()]
    C[4,4:6] = [float(cij) for cij in wamitdata[loc+3].split(':')[1].split()]
    C = (C + C.transpose() - eye(6,6)*C.diagonal())*rho*g
            
    # Get Added Mass and Damping Coefficients
    A, B = [zeros((len(T),6,6), float) for i in range(0,2)]
    for l, loc in enumerate(ADDEDMA):
        for line in wamitdata[loc+3:]:
            if len(line.split()) > 0:
                string = "(" + (',').join(line.split()) + ")"
                i,j,aij,bij = eval(string)
                A[l][i-1][j-1]  = aij*rho # will need to consider if
                B[l][i-1][j-1]  = bij*rho*w[l] # only 1 half is printed
            else: break
            
    # Read Directional Data Groups
    Hask   = read_dir_group(T,Dir,HASKIND, wamitdata,6)
    Diff   = read_dir_group(T,Dir,DIFFRACT,wamitdata,6)
    Resp   = read_dir_group(T,Dir,RESPONSE,wamitdata,6)
    Driftm = read_dir_group(T,Dir,DRIFTMOM,wamitdata,3)
    Driftp = read_dir_group(T,Dir,DRIFTPRE,wamitdata,6)

    # Find Symmetry
    sym = (wamitdata[SymXY[0]].split("Symmetr"))[1]; isys = None
    if   "X=0" in sym and "Y=0" in sym: sym = "X&Y"
    elif "Y=0" in sym:                  sym = "Y=0"
    elif "X=0" in sym:                  sym = "X=0"
    else: sym = None

    # Find Water Depth
    depth = wamitdata[Depth[0]].split(":")[1].split()[0]
    if depth == "infinite": depth = "9999"
    depth = float(depth)

    # Check if any wavedrift frequencies to smooth (temporary implementation)
    if skiplist is not None and Driftp is not None:
        SL = eval(skiplist)
        print(SL)
        for id in SL: Driftp[id-1,:,:] = (Driftp[id-2,:,:] + Driftp[id,:,:])/2.


    # fill dictionary
    VesselData = {"Headings":Dir,"Periods":T,"Wavenumbers":wavek,"KMatrix":C,
                  "AddedMass":A, "Damping":B, "rho":1025., "g":9.81, 
                  "Symmetry":sym, "Mass":M, "Depth": depth}
    if Hask   is not None: VesselData["Fexc_H"]  = Hask*g*rho 
    if Diff   is not None: VesselData["Fexc_D"]  = Diff*g*rho 
    if Resp   is not None: VesselData["R.A.O"]   = Resp 
    if Driftm is not None: VesselData["Drift_M"] = Driftm*g*rho 
    if Driftp is not None: VesselData["Drift_P"] = Driftp*g*rho
    return VesselData




def read_wamit2(filename, ampl, skiplist=None):
    """ Returns a dictionary of Hydrodynamic Vessel Data read from WAMIT 
        Replacing the heave transfer functions with those from WAMOF.
        As it stands this routine is temporary.
        A more generic calling of a WAMOF module will be written
    """

    print("Opening %s\n" % filename)
    wamitdata = open(filename, "r").readlines()
            
    # Get locations of various strings in the wamitdata
    Periods = find_locations("Wave period", wamitdata)
    Wavenum = find_locations("Wavenumber",  wamitdata)
    Heading = find_locations("Wave Heading",wamitdata)
    Gravity = find_locations("Gravity",     wamitdata)
    Length  = find_locations("Length",      wamitdata)
    Depth   = find_locations("depth",       wamitdata)
    Density = find_locations("density",     wamitdata)
    panels  = find_locations("panels",      wamitdata)
    SymXY   = find_locations("Symmetr",     wamitdata)
    XBODY   = find_locations("XBODY",       wamitdata)
    Volumes = find_locations("Volumes",     wamitdata)
    CB      = find_locations("Center of Buoyancy",     wamitdata)
    H20Grav = find_locations("restoring coefficients", wamitdata)
    CG      = find_locations("Center of Gravity",      wamitdata)
    Mass    = find_locations("mass matrix",            wamitdata)
    Damping = find_locations("damping matrix",         wamitdata)
    Stiff   = find_locations("stiffness matrix",       wamitdata)
    ADDEDMA = find_locations("ADDED-MASS AND DAMPING COEFFICIENTS",    wamitdata)
    HASKIND = find_locations("HASKIND EXCITING FORCES AND MOMENTS",    wamitdata) 
    DIFFRACT= find_locations("DIFFRACTION EXCITING FORCES AND MOMENTS",wamitdata) 
    RESPONSE= find_locations("RESPONSE AMPLITUDE OPERATORS",           wamitdata)
    DRIFTMOM= find_locations("DRIFT FORCES (Momentum Conservation)",   wamitdata)
    DRIFTPRE= find_locations("DRIFT FORCES (Pressure Integration)",    wamitdata)
            
    # Read periods, wavenumbers and compute radian wave frequencies
    T = array([float(wamitdata[loc].split()[4]) for loc in Periods])
    wavek = array([float(wamitdata[loc].split()[8]) for loc in Periods])
    w = 2 * pi / T
            
    # get wave headings (hidden bug that wamit.out has headings ascending)
    Dir = array([float(wamitdata[loc].split()[4]) for loc in Heading])
    Dir = sort(array(list(set(Dir)))) 
            
    # Quantities for dimensionalization 
    g   = 9.81; rho = 1025; sf = 1.0
    if float(wamitdata[Density[0]].split("density:")[1]) < 2.0: sf = 1000.
            
    # get mass matrix
    M = zeros((6,6))
    if len(Mass) > 0:
        loc = Mass[0]; 
        for i, line in enumerate(wamitdata[loc+1:loc+7]):
            M[i,:] = [float(j) for j in line.split()]
        M = M * sf
        #set_printoptions(precision=2)#; print M 
    # get hydrostatic and gravitational restoring coefficients
    loc = H20Grav[0]; C = zeros((6,6))
    C[2,2:5] = [float(cij) for cij in wamitdata[loc+1].split(':')[1].split()]
    C[3,3:6] = [float(cij) for cij in wamitdata[loc+2].split(':')[1].split()]
    C[4,4:6] = [float(cij) for cij in wamitdata[loc+3].split(':')[1].split()]
    C = (C + C.transpose() - eye(6,6)*C.diagonal())*rho*g
            
    # Get Added Mass and Damping Coefficients
    A, B = [zeros((len(T),6,6), float) for i in range(0,2)]
    for l, loc in enumerate(ADDEDMA):
        for line in wamitdata[loc+3:]:
            if len(line.split()) > 0:
                string = "(" + (',').join(line.split()) + ")"
                i,j,aij,bij = eval(string)
                A[l][i-1][j-1]  = aij*rho # will need to consider if
                B[l][i-1][j-1]  = bij*rho*w[l] # only 1 half is printed
            else: break
            
    # Read Directional Data Groups
    Hask   = read_dir_group(T,Dir,HASKIND, wamitdata,6)
    Diff   = read_dir_group(T,Dir,DIFFRACT,wamitdata,6)
    Resp   = read_dir_group(T,Dir,RESPONSE,wamitdata,6)
    Driftm = read_dir_group(T,Dir,DRIFTMOM,wamitdata,3)
    Driftp = read_dir_group(T,Dir,DRIFTPRE,wamitdata,6)

    for i, h in enumerate(Dir):
        strh = "%.2f" % h
        wamofile = filename[:-4] + ".dat_WAMOF_Heave_A" + ampl + "_Dir"+strh+".dat"
        d = loadtxt(wamofile,skiprows=1)
        per, hp, pp, hv, pv = d.transpose()
        pv = -pv
        heave_wamof = hv*exp(1j*pv*pi/180.)
        if any(abs(angle(heave_wamof)*180./pi - pv) < 1.E-02):
            for a,b,c,d in zip(angle(heave_wamof)*180./pi, pv, heave_wamof, hv):
                print("%7.2f %7.2f %12.3e %12.3e %12.3e" % (a, b, c.real, c.imag, d))
        # check periods
        if any(abs(per - T) > 1):
            print("Reversing Periods in WAMOF file ...")
            for a,b in zip(per,T):
                print("%8.3f %8.3f" % (a,b))
            heave_wamof[:] = heave_wamof[::-1]
        Resp[:,i,2] = heave_wamof[:]


    # Find Symmetry
    sym = (wamitdata[SymXY[0]].split("Symmetr"))[1]; isys = None
    if   "X=0" in sym and "Y=0" in sym: sym = "X&Y"
    elif "Y=0" in sym:                  sym = "Y=0"
    elif "X=0" in sym:                  sym = "X=0"
    else: sym = None

    # Find Water Depth
    depth = float(wamitdata[Depth[0]].split(":")[1].split()[0])

    # Check if any wavedrift frequencies to smooth (temporary implementation)
    if skiplist is not None and Driftp is not None:
        SL = eval(skiplist)
        print(SL)
        for id in SL: Driftp[id-1,:,:] = (Driftp[id-2,:,:] + Driftp[id,:,:])/2.

    # fill dictionary
    VesselData = {"Headings":Dir,"Periods":T,"Wavenumbers":wavek,"KMatrix":C,
                  "AddedMass":A, "Damping":B, "rho":1025., "g":9.81, 
                  "Symmetry":sym, "Mass":M, "Depth": depth}
    if Hask   is not None: VesselData["Fexc_H"]  = Hask*g*rho 
    if Diff   is not None: VesselData["Fexc_D"]  = Diff*g*rho 
    if Resp   is not None: VesselData["R.A.O"]   = Resp 
    if Driftm is not None: VesselData["Drift_M"] = Driftm*g*rho 
    if Driftp is not None: VesselData["Drift_P"] = Driftp*g*rho
    return VesselData
















def amalg_wamit(options,files):
    """ The function amalgamates a list of wamit files """
    try:
        if len(files) == 0: raise Usage("no files specified")
        ListOfBlocks  = []
        ListOfPeriods = []
        for file in files:
            data = open(file,"r").readlines()
            
            # add data blocks of wave period data to ListOfBlocks
            loc = find_locations(file,"Wave period")
            if len(loc) == 0: 
                raise Usage("'Wave period' string not found on %s" % file)
            header = data[:loc[0]]
            for i in range(0,len(loc)-1):
                ListOfBlocks.append(WavePeriodDataBlock(data[loc[i]:loc[i+1]]))
            ListOfBlocks.append(WavePeriodDataBlock(data[loc[len(loc)-1]:]))

            # extract the header string listing the periods
            loc = find_locations(file,"Period")
            if len(loc) != 1: 
                raise Usage("Only 1 'Period' string should be in %s: %i found"
                                        % (len(loc),file))
            for i, line in enumerate(data[loc[0]+1:]):
                if len(line.strip()) == 0:
                   block = data[loc[0]+1:loc[0]+1+i]
                   break
            for line in block:
                ListOfPeriods.append(WavePeriodHeader(line))
            
        # Now sort the lists in Period ascending order
        ListOfBlocks.sort()
        ListOfPeriods.sort()
        ListOfBlocks  = remove_waveduplicates(ListOfBlocks)
        ListOfPeriods = remove_waveduplicates(ListOfPeriods)
        
        # Now export to a newfile
        fout = open(options.ofile,"w")
        fout.writelines(data[:loc[0]+1])
        for period in ListOfPeriods:
            fout.write("%s" % period.line)
        loco = find_locations(file,"Wave period")
        fout.writelines(data[loc[0]+1+i:loco[0]])
        
        for block in ListOfBlocks:
            fout.writelines(block.data)
            
    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        return 2


def plot_wamit(options,arguments):
    """ plots a wamit.out file """
    
    if options.skiplist is not None:
        data    = read_wamit(arguments[0],options.skiplist) 
    else:
        data    = read_wamit(arguments[0]) # N, kg, m, s
    Dir     = data["Headings"]
    T       = data["Periods"]
    w       = 2*pi/T
    wavek   = data["Wavenumbers"]
    A       = data["AddedMass"]
    B       = data["Damping"]
    
    # for legend increase x range
    xmax  = 40. #70. #1.5*max(T)
    Modes = ["Surge","Sway","Heave","Roll","Pitch","Yaw"] 
    os.system("mkdir figures")
    systemid = options.name #+ " (T=" + options.draft + "m)\n"
    #mks = ["o",".","+","^","s","p","*",">","v","d","x","D","H"]
    mks = []
    for m in Line2D.markers:
        try:
            if len(m) == 1 and m != ' ':
                mks.append(m)
        except TypeError: 
            pass

    mks = mks + [
        r'$\lambda$',
        r'$\bowtie$',
        r'$\circlearrowleft$',
        r'$\clubsuit$',
        r'$\checkmark$']
    
    #markers = iter(marks)
    
    # Plot Wave Excitation Coefficients
    ftype = 3*[("kN/m","Force")] + 3*[("kNm/m","Moment")]
    dtype = [("Haskind relations","Fexc_H"), ("Diffraction potential","Fexc_D")]
    for dt in dtype:
        if data.get(dt[1],None) is not None:
            print("plotting wave excitation coefficients using " + dt[0]); 
            Fexc = data[dt[1]]
            for m, mode in enumerate(Modes):
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
                figtext(0.5,0.94,systemid,ha='center',color='red')
                title("1st Order Wave Excitation " + ftype[m][1] 
                    + " Coefficents in " + mode + "\n(computed from " + dt[0]+")")
                for i, d in enumerate(Dir):
                    plot(T,abs(Fexc[:,i,m]/1000.),marker=mks[i])
                legend([str(x) + ' deg' for x in Dir ],loc=(1.03,0.0))
                xlabel("Period [s]")
                ylabel(ftype[m][1] +
                        " / Amplitude of Incident Wave " + ftype[m][0])
                #xlim(0.,xmax)
                xlim(2.,xmax)
                #ind = nonzero(T>=2)[0]
                #ylim(0.,1.5*abs(Fexc[ix_(ind),:,m]).max()/1000.)
                savefig("figures/"+dt[1]+"_"+mode+".png")
                savefig("figures/"+dt[1]+"_"+mode+".eps")
                clf()


    for dt in dtype:
        if data.get(dt[1],None) is not None:
            print("plotting phase of wave excitation coefficients using " + dt[0]); 
            Fexc = data[dt[1]]
            for m, mode in enumerate(Modes):
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
                figtext(0.5,0.94,systemid,ha='center',color='red')
                title("Phase of 1st Order Wave Excitation " + ftype[m][1] 
                    + " Coefficents in " + mode + "\n(computed from " + dt[0]+")")
                for i, d in enumerate(Dir):
                    plot(T,angle(Fexc[:,i,m])*180./pi,marker=mks[i])
                legend([str(x) + ' deg' for x in Dir ],loc=(1.03,0.0))
                xlabel("Period [s]")
                ylabel("Phase Angle [deg]")
                #xlim(0.,xmax)
                xlim(2.,xmax)
                #ind = nonzero(T>=2)[0]
                #ylim(0.,1.5*abs(Fexc[ix_(ind),:,m]).max()/1000.)
                savefig("figures/"+dt[1]+"_"+'Phase'+mode+".png")
                savefig("figures/"+dt[1]+"_"+'Phase'+mode+".eps")
                clf()



    # Plot Response Amplitude Operators
    if data.get("R.A.O",None)   is not None:
        print("plotting R.A.Os")
        Resp  = data["R.A.O"]
        dt = 3*["Wave Amplitude [-]"]+3*["Wave Slope, ka [-]"]
        for m, mode in enumerate(Modes):
            figure(figsize=(11,6))
            axes([0.15,0.1,0.65,0.75])
            #ax = gca()
            #ax.semilogx()
            #ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.f"))
            #ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
            #ax.set_xticks([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70])
            #ax.set_xticks([3,4,5,6,7,8,9,10,20,30,40,50,60,70])
            #ax.xaxis.grid(True, which='minor')
            #ax.xaxis.grid(True, which='major', color='k', linestyle='--')
            #ax.yaxis.grid(True, which='major')
            figtext(0.5,0.94,systemid,ha='center',color='red')
            #sf = ones(len(wavek)) 
            title("1st Order " + mode + " Response / " + dt[m] +
                    "\n('Response Amplitude Operator' (R.A.O.))")
            if m > 2:
                for i, d in enumerate(Dir):
                    plot(T,abs(Resp[:,i,m])/wavek[:],marker=mks[i])
            else:
                for i, d in enumerate(Dir):
                    plot(T,abs(Resp[:,i,m]),marker=mks[i])            
            grid(True)
            legend([str(x) + ' deg' for x in Dir ], loc=(1.03,0.0))
            xlabel("Period [s]")
            ylabel(mode + " Response / " + dt[m])
            xlim(0.,xmax)
            #xlim(3.,xmax)
            #ind = nonzero(T<=40)[0]
            #print ind
            #sys.exit(-1)
            #ylim(0., 1.5*abs(Resp[ix_(ind),:,m]).max())
            savefig("figures/"+"Response_"+mode+".png")
            savefig("figures/"+"Response_"+mode+".eps")
            clf()


    # Plot Response Amplitude Operators
    if data.get("R.A.O",None)   is not None:
        print("plotting R.A.Os phase")
        Resp  = data["R.A.O"]
        dt = 3*["Wave Amplitude [-]"]+3*["Wave Slope, ka [-]"]
        for m, mode in enumerate(Modes):
            figure(figsize=(11,6))
            axes([0.15,0.1,0.65,0.75])
            #ax = gca()
            #ax.semilogx()
            #ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.f"))
            #ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
            #ax.set_xticks([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70])
            #ax.set_xticks([3,4,5,6,7,8,9,10,20,30,40,50,60,70])
            #ax.xaxis.grid(True, which='minor')
            #ax.xaxis.grid(True, which='major', color='k', linestyle='--')
            #ax.yaxis.grid(True, which='major')
            figtext(0.5,0.94,systemid,ha='center',color='red')
            #sf = ones(len(wavek)) 
            title("Phase of 1st Order " + mode + " Response Transfer Functions")
            for i, d in enumerate(Dir):
                plot(T,angle(Resp[:,i,m])*180./pi,marker=mks[i])
            grid(True)
            legend([str(x) + ' deg' for x in Dir ], loc=(1.03,0.0))
            xlabel("Period [s]")
            ylabel("Phase Angle [deg]")
            xlim(0.,xmax)
            #xlim(3.,xmax)
            #ind = nonzero(T>=3)[0]
            #ylim(0., 1.5*abs(Resp[ix_(ind),:,m]).max()/1000.)
            savefig("figures/"+"Response_Phase"+mode+".png")
            savefig("figures/"+"Response_Phase"+mode+".eps")
            clf()



    # Plot mean wave drift coefficients
    ftype = 3*[("kN/m^2","Force")] + 3*[("kNm/m^2","Moment")]
    dtype = [("momentum","Drift_M"), ("pressure","Drift_P")]
    for id, dt in enumerate(dtype):
        if data.get(dt[1],None) is not None:
            print("plotting drift coefficients from " + dt[0] + " integration"); 
            Drift = data[dt[1]]
            for m, mode in enumerate(Modes):
                if id == 0 and 1 < m < 5: continue
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
                figtext(0.5,0.94,systemid,ha='center',color='red')
                ind = nonzero(T>=2.5)[0]
                title("Mean Drift Force Coefficient in " + mode +
                    "\n(computed from " + dt[0] + " integration)")
                for i, d in enumerate(Dir):
                    plot(T[ind],Drift[ind,i,m].real/1000.,marker=mks[i])
                grid(True)
                legend([str(x) + ' deg' for x in Dir ], loc=(1.03,0.0))
                xlabel("Period [s]")
                ylabel(ftype[m][1] + 
                    " / Amplitude Squared of Incident Wave " + ftype[m][0])
                #xlim(0.,xmax)
                xlim(2.,xmax)
                ind = nonzero(T>=2.5)[0]
                ylim(1.5*(Drift[ix_(ind),:,m].real).min()/1000.,
                     1.5*(Drift[ix_(ind),:,m].real).max()/1000.)
                savefig("figures/"+dt[1]+"_"+mode+".png")
                savefig("figures/"+dt[1]+"_"+mode+".eps")
                clf()

    # Plot Added Mass and Damping Coefficients
    dtype = [("Added Mass","A","^2","acceleration"),("Damping", "B","","velocity")]
    for k, C in enumerate([A,B]):
        print("plotting " + dtype[k][0] + " coefficients"); 
        for i, mi in enumerate(Modes):
            for j, mj in enumerate(Modes):  
                if all(C[:,i,j]==0): continue
                figure(figsize=(11,6))
                axes([0.15,0.1,0.65,0.75])
                ax = gca()
                ax.semilogx()
                ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.f"))
                ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
                ax.set_xticks([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70])
                ax.xaxis.grid(True, which='minor')
                ax.xaxis.grid(True, which='major', color='k', linestyle='--')
                ax.yaxis.grid(True, which='major')
                figtext(0.5,0.94,systemid,ha='center',color='red')
                plot(T,C[:,i,j]/1000.,marker='x')
                grid(True)
                t1 = "1st Order Wave Radiation '" + dtype[k][0] + "'"
                t2 = "\nper (due to) unit amplitude of body "+ dtype[k][3]+" in "
                l1 = dtype[k][1] + str(i+1) + str(j+1)
                legend([l1], loc=(1.03,0.0))
                xlabel("Period [s]")
                if (i < 3) and (j < 3):            
                    title(t1 + " Force in " + mi + t2 + mj)
                    ylabel(l1 + " [kN/(m/s"+dtype[k][2] + ")]")
                if (i >= 3) and (j < 3):
                    title(t1 + " Moment in " + mi + t2 + mj)
                    ylabel(l1 + " [kNm/(m/s"+dtype[k][2] + ")]")
                if (i >= 3) and (j >= 3):
                    title(t1 + " Moment in " + mi + t2 + mj)
                    ylabel(l1 + " [kNm/(rad/s"+dtype[k][2] + ")]")
                if (i < 3) and (j >= 3):
                    title(t1 + " Force in " + mi + t2 + mj)
                    ylabel(l1 + " [kN/(rad/s"+dtype[k][2] + ")]")
                xlim(0.,xmax)
                savefig("figures/"+dtype[k][1]+str(i+1)+str(j+1)+".png")
                savefig("figures/"+dtype[k][1]+str(i+1)+str(j+1)+".eps")
                clf()

def exportbeamer(options,arguments):
    """ Exports a beamer presentation. """
    wamdoc = beamer(name = options.pdfbeamer,
                    title= "Diffraction Analysis for %s" % options.name)
    wamdoc.open()
    wamdoc.addSection("1st Order Diffraction Analysis")
    Modes = ["Surge","Sway","Heave","Roll","Pitch","Yaw"]

    # Add Wave Excitation Coefficients
    wamdoc.addSubsection("Wave Excitation Force Coefficients")
    wamdoc.addSubsubsection("Amplitudes")
    for mode in Modes:
        wamdoc.addFrame("Moduli of Wave Excitation Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Fexc_D_%s.png" % mode])

    wamdoc.addSubsubsection("Phases")
    for mode in Modes:
        wamdoc.addFrame("Phases of Wave Excitation Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Fexc_D_Phase%s.png" % mode])

    # Add R.A.Os
    wamdoc.addSubsection("Response Amplitude Operators")
    wamdoc.addSubsubsection("Amplitudes")
    for mode in Modes:
        wamdoc.addFrame("Moduli of Response Amplitude Operators", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Response_%s.png" % mode])
    wamdoc.addSubsubsection("Phases")
    for mode in Modes:
        wamdoc.addFrame("Phases of Response Amplitude Operators", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Response_Phase%s.png" % mode])

    # Add Mean Wave Drift Coefficients
    wamdoc.addSubsection("Mean Wave Drift Force Coefficients")
    wamdoc.addSubsubsection("Pressure Integration")
    for mode in Modes:
        wamdoc.addFrame("Mean Wave Drift Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Drift_P_%s.png" % mode])
 
    wamdoc.addSubsubsection("Momentum Conservation (Far-field formulation)")
    for mode in Modes[0:2] + Modes[5:]:
        wamdoc.addFrame("Mean Wave Drift Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Drift_M_%s.png" % mode])


    # Add Added Mass or Damping Coefficients
    wamdoc.addSubsection("Added Mass and Damping Coefficients")
    Modes = ["11", "15", "22", "24", "33", "42", "44","51","55","66"]
    for mode in Modes:
        wamdoc.addFrame("Added Mass Coefficients", 
                        "A%s" % mode, 
                        imagelist=["figures/A%s.png" % mode])
    for mode in Modes:
        wamdoc.addFrame("Damping Coefficients", 
                        "B%s" % mode, 
                        imagelist=["figures/B%s.png" % mode])

    wamdoc.close()
    sp.Popen("pdflatex %s > run.log" % wamdoc.name,shell=True).wait()
    sp.Popen("pdflatex %s > run.log" % wamdoc.name,shell=True).wait()
    #for ext in [".aux",".log",".nav",".snm",".tex",".toc",".out"]:
    #    sp.Popen("del %s" % wamdoc.name.strip(".tex") + ext,
    #             shell=True).wait()


if __name__ == '__main__':
    sys.exit(main())
