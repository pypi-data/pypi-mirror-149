from typing import Dict, List, Optional, Any, Tuple
import freesif #from freesif import open_sif    
import shutil
import numpy as np
import sys
import os
import uuid
import random
import string

def id_generator(size:int=6, chars:str=string.ascii_uppercase + string.digits) -> str:
    """Generates a random string for use as a unique identifier (id).

    Args:
        size (int, optional): Length of random string (id) to be generated. Defaults to 6.
        chars (str, optional): String from which to randomly extract characters for the id. Defaults to string.ascii_uppercase+string.digits.

    Returns:
        str: id
        
    TODO: Move to an external library
    """
    return ''.join(random.choice(chars) for _ in range(size))

def open_sif(folder:str, filename:str)->Tuple[freesif.File, str]:
    """Opens a wadam sif file. This is wrapper to freesif's open_sif function that allows for
    '.' separators in the filename. Should perhaps be extended to include arbitrary extensions.

    Args:
        folder (str): folder containing sif file
        filename (str): name of sif file

    Returns:
        (sif object, temporary filename): Tuple containing the sif object and temporary filename
    """
    id = id_generator()
    filename_tmp = "r" + id + filename[:-4].replace(".","_") + '.SIF'
    shutil.copyfile(f"{folder}/{filename}", filename_tmp)
    # Open the sif and read the data
    sif = freesif.open_sif(filename_tmp)
    return sif, filename_tmp


def get_wadam_strings(folder:str, filename:str, wdfactors:List[float]=[1]*6, 
    pmin:List[float]=[10]*6, pmax:List[float]=[30]*6, ppeak:List[float]=[18.0]*6, 
    scaling:List[str] = ["cos2"]*6, return_arrays:bool=False, 
    return_hz_dirs:bool=False,imosym:int=1,exwave_params:Dict={})->List[List[Any]]:
    """Reads a WADAM SIF file and returns [raoStrings, wavedriftStrings]
    which are lists of length 6, where the 6 entries relate to the degrees of 
    freedom of body motion (surge, sway, heave, roll, pitch, yaw) respectively. 
    
    Each entry is a string which is in SIMO (sys.dat) format, where e.g.
        raoStrings[0] is the surge RAO as a single string
        wavedriftStrings[3] is the mean wavedrift coefficients in roll.
        
    In addition to the strings, the user can get the coefficients as value arrays,
    and can request the frequencies (Hz) and directions (degrees)::
    
        raoStr, wdStr = get_wadam_strings(folder,filename)
        freqs, dirs, raoStr, wdStr = get_wadam_strings(folder,filename,return_hz_dirs=True)
        freqs, dirs, raoStr, wdStr, raos, wds = get_wadam_strings(folder,filename,return_hz_dirs=True, return_arrays=True)      

    Optionally the user can scale the wave drift coefficients using a scaling function.
    The scaling function is specified by the "scaling" argument and can take the values:
    
        "constant": constant scaling
        "linear":   linear scaling. At wave periods <= pmin and >= pmax the scaling factor takes the value of 1.0
                    i.e. no scaling. At wave period ppeak, where pmin < ppeak < pmax, the scaling factor takes a
                    value specified by the corresponding entry in the wdfactors list for the response.
        "cos2" :    Similar to linear except the scaling function between pmin/pmax and ppeak is cosine-squared
        "gauss":    Similar to cos2 except the scaling function is Guassian and the scaling values at pmin/pmin
                    10% the value specified by the wdfactor array
        "exwave":   Uses TR2396 exwave formula. Requires a dictionary of exwave_params containing
                        {"Hs": significant wave height in m,
                         "D0": column diameter,
                         "U":  current speed,
                         "ncols": number of columns}

    Args:
        folder (str): folder of the SIF file
        filename (str): filename of the SIF file
        wdfactors (List[float], optional): Maximum value of scaling function to apply at ppeak. Defaults to [1]*6.
        pmin (List[float], optional): Minimum period for scaling. Defaults to [10]*6.
        pmax (List[float], optional): Maximum period for scaling. Defaults to [30]*6.
        ppeak (List[float], optional): Peak period for scaling. Defaults to [18.0]*6.
        scaling (List[str], optional): Type of scaling. Defaults to ["cos2"]*6.
        return_arrays (bool, optional): Set true to return values of raos and wavedrift coefficients. Defaults to False.
        return_hz_dirs (bool, optional): Set True to return wave frequencies (Hz) and directions. Defaults to False.

    Returns:
        List[List[Any]]: See docstring
    """
    # Read the mean wave drift coefficients and raos on the SIF file
    sif, filename_tmp = open_sif(folder,filename)
    periods = sif.get_periods()
    directions = sif.get_directions()
    omegas = sif.get_angular_freqs()
    raos = sif.get_motion_raos()
    pressure = sif.get_meandrift()
    momentum = sif.get_horiz_meandrift()
    sif.close()
    os.remove(filename_tmp)
    
    # Reformat with increasing frequency    
    raos = raos[:, :, ::-1] # flip the last field
    momentum = momentum[:,:,::-1]
    pressure = pressure[:,:,::-1]
    periods = periods[::-1] # for consistency (superfluous for function)
    omegas = omegas[::-1]
    
    # Compile wavedrift as a mixture of momentum and pressure
    wavedrift = pressure
    wavedrift[0] = momentum[0]
    wavedrift[1] = momentum[1]
    wavedrift[5] = momentum[2]
    wavedrift = wavedrift / 1000. 


    # Establish some blending functions to scale the wavedrifts
    alpha = np.zeros((6,len(periods))) # storage for blending function
    for i in range(0, 6):
        print(i, scaling[i])
        ix_lower = (periods >= pmin[i]) & (periods <= ppeak[i]) 
        ix_upper = (periods <= pmax[i]) & (periods >= ppeak[i])
        coord_lower = 1-(ppeak[i]-periods[ix_lower])/(ppeak[i] - pmin[i])
        coord_upper = 1-(periods[ix_upper]-ppeak[i])/(pmax[i] - ppeak[i])
        if scaling[i] == "constant":
            alpha[i,:] = 1
        if scaling[i] == "linear":
            alpha[i,ix_lower] = coord_lower
            alpha[i,ix_upper] = coord_upper
        if scaling[i] == "cos2":
            alpha[i,ix_lower] = (0.5*(1 - np.cos(coord_lower*np.pi)))**2
            alpha[i,ix_upper] = (0.5*(1 - np.cos(coord_upper*np.pi)))**2
        if scaling[i] == "gauss":
            fwtm_lower = 2*(ppeak[i]-pmin[i]) # full width at tenth of the maximum
            fwtm_upper = 2*(pmax[i]-ppeak[i]) # full width at tenth of the maximum
            c_lower = fwtm_lower/4.29193
            c_upper = fwtm_upper/4.29193
            alpha_lower = np.exp(-(periods-ppeak[i])**2/2/c_lower**2)
            alpha_upper = np.exp(-(periods-ppeak[i])**2/2/c_upper**2)
            alpha[i] = np.where(periods < ppeak[i], alpha_lower, alpha_upper)
        if scaling[i] == "exwave":
            # TODO: requires hs snd other arguments, disallow for now
            hs = exwave_params["Hs"]
            D0 = exwave_params["D0"] #96
            U = exwave_params["U"] #0.73 # would need to enter
            G = 10 # s
            Cp = 0.25 # s/m
            ncols = exwave_params["ncols"]
            Dsum = D0*ncols 
            w = 2*np.pi/periods
            k = w**2/9.80665 # use deep water
            p = np.exp(-1.25*(k*D0)**2)
            B = k*p*Dsum
            exwave_params["scale"] = (1+Cp*U)
            exwave_params["loc"] = B*(G*U +  hs)  

    # if the factor is 1.0 want no change. If factor 1.1 we want some change
    wavedrift_original = wavedrift*1.0 # make a copy for checking (then remove!)
    wavedrift_peak = wavedrift*1.0 # make storage for peak scaling
    for idof in range(len(raos)):
        for idir in range(len(directions)):
            if scaling[idof] == "exwave":
                wavedrift[idof,idir] = wavedrift_original[idof,idir]*exwave_params["scale"] + \
                                            exwave_params["loc"] 
            else:
                wavedrift_peak[idof,idir] = wavedrift_original[idof,idir]*wdfactors[idof]
                wavedrift[idof,idir] = alpha[idof]*wavedrift_peak[idof,idir] + (1-alpha[idof])*wavedrift_original[idof,idir]

    rao_string = []
    rao_string.append("FIRST ORDER MOTION TRANSFER FUNCTION\n\n")
    rao_string.append(f"{directions.size} {omegas.size} {imosym} 2")
    rao_string.append("WAVE DIRECTIONS MOTION TRANSFER FUNCTION")
    rao_string.append("\n".join([f"{idir+1:2d}  {d:.1f}" for idir, d in enumerate(directions)]))
    rao_string.append("WAVE FREQUENCIES MOTION TRANSFER FUNCTION")
    rao_string.append("\n".join([f"{iw+1:2d}  {w:.10e}" for iw, w in enumerate(omegas)]))
    names = "SURGE SWAY HEAVE ROLL PITCH YAW".split()
    for idof, name in enumerate(names):
        rao_string.append(f"{name} MOTION TRANSFER FUNCTION")
        rao_string.append('\n'.join([f"{idir+1:d}  {iw+1:d}  {np.abs(raos[idof,idir,iw]):.10e} {np.angle(raos[idof,idir,iw])*180./np.pi:.10e}" 
                            for idir in range(directions.size) for iw in range(omegas.size)]))
    rao_string = "\n".join(rao_string)

    wd_string = []
    wd_string.append("SECOND ORDER WAVE DRIFT FORCES\n\n")
    wd_string.append(f"{directions.size} {omegas.size} {imosym}")
    wd_string.append("WAVE DIRECTIONS DRIFT COEFFICIENTS")
    wd_string.append("\n".join([f"{idir+1:2d}  {d:.1f}" for idir, d in enumerate(directions)]))
    wd_string.append("WAVE FREQUENCIES DRIFT COEFFICIENTS")
    wd_string.append("\n".join([f"{iw+1:2d}  {w:.10e}" for iw, w in enumerate(omegas)]))
    for idof, name in enumerate(names):
        wd_string.append(f"{name} WAVE DRIFT COEFFICIENTS")
        wd_string.append('\n'.join([f"{idir+1:d}  {iw+1:d}  {wavedrift[idof,idir,iw]:.10e}" 
                            for idir in range(directions.size) for iw in range(omegas.size)]))
    wd_string = "\n".join(wd_string)    

    dataset = [1/periods, directions] if return_hz_dirs else []
    dataset += [rao_string, wd_string]
    dataset += [raos, wavedrift] if return_arrays else []
    return dataset



def read_SIF_rao(folder:str, filename:str, wadir:float, 
                 mapping_index:List[int]=[0,1,2,3,4,5],
                 mapping_sign:List[int]=[1,1,1,1,1,1]):
    """Returns the RAOs on the SIF file for a given wave direction.

    Args:
        folder (str): folder containing the SIF file
        filename (str): filename of the SIF file
        wadir (float): wave direction of interest
        mapping_index (List[int], optional): Maps the degrees of freedom to another order. 
                Defaults to [0,1,2,3,4,5], e.g. [1,0,2,4,3,5] surge<=>sway, roll<=>pitch. 
                Wadir still needs to be correct for unmapped setup. 
        mapping_sign (List[int], optional): Applies a sign change to the mapped setup. 

    Returns:
        [type]: [description]
    """
    
    # Read data
    sif, filename_tmp = open_sif(folder, filename)
    periods = sif.get_periods()
    directions = sif.get_directions()
    raos = sif.get_motion_raos()
    sif.close()
    os.remove(filename_tmp)
    # Extract wave direction and scale.
    ix = np.nonzero(wadir==directions)
    factor = [1,1,1,180./np.pi,180./np.pi,180./np.pi]
    # Correcting for the chosen coordinate system :/
    return 1./periods[::-1], [mapping_sign[dof]*factor[dof]*np.squeeze(raos[dof, ix, ::-1]) for dof in mapping_index]



def get_wave_force_coefficients(folder:str, filename:str, as_simo_string=True, 
                                alpha=[1.0]*6, imosym=1, as_kN=True, blend=[1,1,1,1,1,1],
                                Be:np.ndarray=np.zeros((6,6)), Ae:np.ndarray=np.zeros((6,6)), 
                                Ce:np.ndarray=np.zeros((6,6)))->Tuple[np.ndarray,np.ndarray,np.ndarray]:
    """Returns the wave force coefficients from a WADAM SIF file. If blend=[0,0,0,0,0,0], the function
    will return values on the SIF file. Allows the user to manipulate the returned values by entering 
    part of the external matrices used in the generation of RAOs, where:
        Ae = External added mass, Be = External damping, Ce = External stiffness
    The remaining part will then be grouped in the wave force coefficients as a "modification". 
    
    Args:
        folder (str): folder containing SIF file
        filename (str): SIF filename
        as_simo_string (bool, optional): Return the coefficients as a simo string for input into a system file. Defaults to True.
        alpha (_type_, optional): Apply a constant scaling factor. Defaults to [1.0]*6.
        imosym (int, optional): Symmetry integer (0: None, 1: Y=0 symmetry, 2: X=0 and Y=0 symmetry). Defaults to 1.
        as_kN (bool, optional): Return as kN. Defaults to True.
        blend (list, optional): Array relating to the 6-DOF. If entry is 1, for that DOF returns coefficients affected by external A, B, C matrices. Defaults to [1,1,1,1,1,1].
        Be (np.ndarray, optional): External 6x6 damping matrix. Defaults to np.array((6,6)).
        Ae (np.ndarray, optional): External 6x6 added mass matrix. Defaults to np.array((6,6)).
        Ce (np.ndarray, optional): External 6x6 stiffness matrix. Defaults to np.array((6,6)).

    Returns:
        Tuple of np.ndarrays: angular frequencies, directions, forces
    """
    
    # experimental hs tp addition
    #import wafo.spectrum.models as wsm
    #S = wsm.Torsethaugen(hs, tp)
    
    sif, filename_tmp = open_sif(folder, filename)
    omegas = sif.get_angular_freqs()
    directions = sif.get_directions()
    X = sif.get_motion_raos()
    Fd = sif.get_excitationforce_raos()
    M = sif.get_bodymass()
    A = sif.get_addedmass()
    B = sif.get_potentialdamping()
    C = sif.get_hydrostatic_restoring()
    #Bv = sif.get_viscousdamping()    
    sif.close()
    os.remove(filename_tmp)
        
    F = np.zeros(Fd.shape, dtype=np.complex)
    alpha = np.array(alpha)
    blend = np.array(blend)
    
    for idir in range(directions.size):
        
        # experimental (perform crude integration to test)
        #H = X[2, idir, ::-1]
        #w = omegas[::-1]
        #Ve = np.sqrt(8/np.pi*np.trapz(S(w)*np.abs(H)**2,w))
        #Bv[2,2] = 0.125*1025*(np.pi*D**2)*Ve
        
        for iw, w in enumerate(omegas):
            lhs_matrix = -w**2*(M+A[:,:,iw]+Ae)+1j*w*(B[:,:,iw]+Be)+(C+Ce)
            raos = X[:, idir, iw]
            F[:,idir,iw] = lhs_matrix@raos*alpha*blend + Fd[:,idir,iw]*alpha*(1-blend)
    
    omegas = omegas[::-1]
    F = F[:,:,::-1]
    
    if as_kN: F = F/1000.
    
    if as_simo_string:
        string = []
        string.append("FIRST ORDER WAVE FORCE TRANSFER FUNCTION\n\n")
        string.append(f"{directions.size} {omegas.size} {imosym} 2")
        string.append("WAVE DIRECTIONS FORCE TRANSFER FUNCTION")
        string.append("\n".join([f"{idir+1:2d}  {d:.1f}" for idir, d in enumerate(directions)]))
        string.append("WAVE FREQUENCIES FORCE TRANSFER FUNCTION")
        string.append("\n".join([f"{iw+1:2d}  {w:.10e}" for iw, w in enumerate(omegas)]))
        names = "SURGE SWAY HEAVE ROLL PITCH YAW".split()
        for idof, name in enumerate(names):
            string.append(f"{name} FORCE TRANSFER FUNCTION")
            string.append('\n'.join([f"{idir+1:d}  {iw+1:d}  {np.abs(F[idof,idir,iw]):.10e} {np.angle(F[idof,idir,iw])*180./np.pi:.10e}" 
                            for idir in range(directions.size) for iw in range(omegas.size)]))
        return "\n".join(string)
    else:
        return omegas, directions, F        
    
