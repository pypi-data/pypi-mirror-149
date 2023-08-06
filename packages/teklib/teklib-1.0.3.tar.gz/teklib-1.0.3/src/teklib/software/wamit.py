#
# Script: Reads RAOs from either SIMO or WAMIT
#

import numpy as np
from ..miscellaneous.io import loadtxt
from ..administration.tools import find_occurrences, timer
from ..miscellaneous.math import interpc
from .common import Record
import sys
import enum 
from abc import ABC, abstractclassmethod
import scipy.optimize as opt
import time 
import os
import typing



class Wamit(object):
    """ Class for working with WAMIT files
    TODO: Implement an effective read (note we can have static functions)
    //TODO: Implement a wave to wave TF transformation to field location
    TODO: Implement a wave to body motion TF transformation to field location
    TODO: Implement a morison element type for general shapes e.g. circles, lines
    //TODO: Implement the EOM   
    TODO: Set external quadratic damping matrices
    //# TODO: Set external stiffness matrix

    Assumes consistent periods in numerical files (no mixing)
    Implemented for one body only
    Phases of exciting forces, motions, pressure and fluid velocity are defined
    relative to the incident-wave elevation at X=Y=0 which is equal to Re(A*e(iwt))=Acos(wt)
    """

    class Motion(enum.IntEnum):
        SURGE = 0
        SWAY = 1
        HEAVE = 2
        ROLL = 3
        PITCH = 4
        YAW = 5

    class Properties(enum.Enum):
        PERIODS = enum.auto()
        DIRECTIONS = enum.auto()
        MASS = enum.auto()
        ADDED_MASS = enum.auto()
        ADDED_MASS_INF = enum.auto()
        ADDED_MASS_ZERO = enum.auto()
        DAMPING = enum.auto()
        EXCITE_HASK = enum.auto()
        EXCITE_DIFF = enum.auto()
        RAOS = enum.auto()
        BODY_PANELS = enum.auto()
        BODY_PRESSURE_TRANSFER_FUNCTIONS = enum.auto()
        STIFFNESS_HYDROGRAV = enum.auto() 
        STIFFNESS_EXTERNAL = enum.auto() 
        DAMPING_EXTERNAL = enum.auto()
        QUADRATIC_DAMPING_EXTERNAL = enum.auto()
        LINEARIZED_QUADRATIC_DAMPING_EXTERNAL = enum.auto() # purely internal
        ADDED_MASS_ZERO_EXTERNAL = enum.auto()
        RETARDATION_FUNCTIONS = enum.auto()
        SLENDER_ELEMENTS = enum.auto()
        NATURAL_PERIODS = enum.auto()
        CRITICAL_DAMPING = enum.auto()
        DISPLACED_VOLUMES = enum.auto()
        MASS_CENTER = enum.auto()
        BUOYANCY_CENTER = enum.auto()
        BODY_POINTS = enum.auto()


    class SlenderElement(object):
        def __init__(self, x1, x2, xref, Cl, Cq, Ca, N):
            """
                Cl - Linear drag coefficients in x, y, z (R^3)
                Cq - Quadratic drag coefficients in x, y, z (R^3)
                Ca - Added mass coefficient in x, y, z (R^3)
            """
            self._x1 = x1
            self._x2 = x2
            self._xref = xref
            self._Cl = Cl
            self._Cq = Cq
            self._Ca = Ca
            # Segment lengths
            self._dl = np.linalg.norm(x2 - x1)/N
            # Segment centroid coordinates 
            self._xp = np.array([x1 + (x2-x1)*(i+0.5)/N for i in range(N)])
            # Compute local unit basis
            xm = x2 - x1
            zm = np.cross(xm, xref-x1)
            ym = np.cross(zm, xm)
            # Compute local basis
            self._ex = xm/np.linalg.norm(xm)
            self._ey = ym/np.linalg.norm(ym)
            self._ez = zm/np.linalg.norm(zm)
            # Compute projection matrix for the perpendicular plane
            xn, yn, zn = self._ex
            self._Pk = np.array([
                [yn**2+zn**2, -xn*yn, -xn*zn],
                [-yn*xn, xn**2+yn**2, -yn*zn],
                [-zn*xn, -zn*yn, xn**2+yn**2]])



        def _compute_force(self, u, A=1.0):
            """ u is a velocity field at points self._xp of size (Np,3), where
                u(xp,:) = velocity of incident at xp wave for RHS term (viscous excitation)
                u(xp,:) = velocity of motion at xp for LHS term (viscous damping)
                xp(Np,3) = body coordinates of points
            """
            e = self.local_basis 
            B = self._Cq*8/3/np.pi*A*(2*np.pi/10)

            xp = self.points
            dl = self._dl
            u = np.einsum("ijkl->klij", u)  # Np,3,nBeta,nPeriod => nBeta,nPeriod,Np,3
            dF = (u@(e.T)*B*dl)@e  # shape nBeta,nPeriod,Np,3
            dM = np.cross(xp, dF, axisa=1, axisb=3) # nBeta,nPeriod,Np,3
            F = np.sum(dF, axis=2) # sum over the 3rd axis (==2nd zero indexed)
            M = np.sum(dM, axis=2) # sum over the 3rd axis (==2nd zero indexed)
            F = np.einsum("ijk->kij", F)
            M = np.einsum("ijk->kij", M)
            F = np.vstack([F, M])
            return F



        @property
        def local_basis(self): return np.vstack([self._ex,self._ey,self._ez])

        @property
        def points(self): return self._xp


    @timer
    def __init__(self, fname, ulen=1.0, density=1.025, g=9.80665, 
                frequency_ascending=False, verbose=False):
        self.fname = fname 
        self._data = {}
        for prop in Wamit.Properties: self._data[prop] = None 
        if os.path.isfile(f"{fname}.1"):
            # Read and unpack added mass (assumes .1 is always there)
            wam = Wamit.read_added_mass_and_damping(f"{fname}.1", ulen, density, frequency_ascending)
            self._data[Wamit.Properties.PERIODS] = wam.periods
            self._data[Wamit.Properties.ADDED_MASS] = wam.added_mass
            self._data[Wamit.Properties.DAMPING] = wam.damping
            self._data[Wamit.Properties.ADDED_MASS_INF] = wam.ainf
            self._data[Wamit.Properties.ADDED_MASS_ZERO] = wam.a0
        if os.path.isfile(f"{fname}.2"):
            # Read and unpack excitation forces from Haskind relations
            wam = Wamit.read_excitation_forces(f"{fname}.2", ulen, density, g, frequency_ascending)
            self._data[Wamit.Properties.EXCITE_HASK] = wam.value
            self._data[Wamit.Properties.DIRECTIONS] = wam.directions
        if os.path.isfile(f"{fname}.3"):
            # Read and unpack excitation forces diffraction potential
            wam = Wamit.read_excitation_forces(f"{fname}.3", ulen, density, g, frequency_ascending)
            self._data[Wamit.Properties.EXCITE_DIFF] = wam.value
            self._data[Wamit.Properties.DIRECTIONS] = wam.directions
        if os.path.isfile(f"{fname}.4"):
            # Read and unpack motion transfer functions
            wam = Wamit.read_raos(f"{fname}.4", ulen, 1, frequency_ascending)
            self._data[Wamit.Properties.RAOS] = wam.value 
        if os.path.isfile(f"{fname}.5p"): # TODO currently assumes ulen=1
            wam = Wamit.read_body_pressure_tfs(f"{fname}.5p")
            self._data[Wamit.Properties.BODY_PRESSURE_TRANSFER_FUNCTIONS] = \
                {"diffraction": wam.h_dif, "radiation": wam.h_rad}
        if os.path.isfile(f"{fname}.pnl"): # TODO currently assumes ulen=1
            wam = Wamit.read_wamit_normals(f"{fname}.pnl") 
            self._data[Wamit.Properties.BODY_PANELS] = wam
        if os.path.isfile(f"{fname}.mmx"):
            # Read and unpack mass data
            wam = Wamit.read_mass_matrix(f"{fname}.mmx")
            self._data[Wamit.Properties.MASS] = wam.mass
            self._data[Wamit.Properties.DAMPING_EXTERNAL] = wam.damping
            self._data[Wamit.Properties.STIFFNESS_EXTERNAL] = wam.stiffness
            self._data[Wamit.Properties.DISPLACED_VOLUMES] = wam.vols
            self._data[Wamit.Properties.MASS_CENTER] = wam.cog
            self._data[Wamit.Properties.BUOYANCY_CENTER] = wam.cob
        if os.path.isfile(f"{fname}.out"):
            # Read stiffness data from out file
            wam = Wamit.read_hydrograv_stiffness(f"{fname}.out", ulen, density, g)
            self._data[Wamit.Properties.STIFFNESS_HYDROGRAV] = wam.stiffness
        # Evaluate retardation functions
        #self._update_retardation_functions()
        # Evaluate natural periods in heave, roll and pitch
        self._compute_natural_periods(verbose)
        # Initial storage for quadratic external damping
        self._data[Wamit.Properties.QUADRATIC_DAMPING_EXTERNAL] = np.zeros((6,6))
        # Initial storage for added mass adjustment
        self._data[Wamit.Properties.ADDED_MASS_ZERO_EXTERNAL] = np.zeros((6,6))
        self._data[Wamit.Properties.LINEARIZED_QUADRATIC_DAMPING_EXTERNAL] = np.zeros((len(self.directions),6,6))


    @property
    def registered_body_points(self):
        assert self._data[Wamit.Properties.BODY_POINTS] is not None, "No body points registered. Use register_body_points"
        return self._data[Wamit.Properties.BODY_POINTS]

    def register_body_points(self, xyz, clean=False):
        """ 
        Register the a numpy array of xyz body point data for the computation of statistics
        Point data given in rows. If just a single point, the xyz is a row vector. 
        The clean option replaces existing points with the new dataset, otherwise
        the points are appended to the existing array of points
        """
        if clean or self._data[Wamit.Properties.BODY_POINTS] is None:
            if xyz.ndim == 1: xyz = np.expand_dims(xyz, axis=0)
            self._data[Wamit.Properties.BODY_POINTS] = xyz
        else:
            self._data[Wamit.Properties.BODY_POINTS] = \
                np.vstack([self._data[Wamit.Properties.BODY_POINTS], xyz])


    def get_raos(self, mode=None, direction=None, return_at_body_points=False,
                return_velocity=False, return_acceleration=False, relative=False):
        """
            Returns the stored wave to motion transfer functions, which need to be precalculated
            using either the solve_EOM function or the solve_stochastic function. 
            The user can request:
                - a specific mode of motion ... all modes of motion returned as default
                - a specific wave direction ... all directions return as default
                - acceleration or velocity to be return instead of the motion raos
            If return_at_body_points=True, the raos are returned at the body point locations 
            The body point locations are registered with register_body_points function.
            if returning at body point locations, only translation modes 0,1,2 available
        """

        # Make assertions
        if direction is not None:
            assert direction in self.directions, "direction not computed, direction interpolation not implemented"    
        if return_at_body_points:
            assert self._data[Wamit.Properties.BODY_POINTS] is not None, "need to register_body_points first"
            if mode is not None:
                assert mode in [Wamit.Motion.SURGE, Wamit.Motion.SWAY, Wamit.Motion.HEAVE], "Need to request Wamit.Motion.SURGE/SWAY/HEAVE"

        nmodes = 3 if return_at_body_points else 6    
        ix = range(nmodes) if mode is None else [mode,]
        jx = range(len(self.directions)) if direction is None else self.directions==direction
        ij = np.ix_(ix, jx)

        if return_at_body_points:
            assert self._data[Wamit.Properties.BODY_POINTS] is not None, "need to register_body_points first"
            X = self.transform_rao(self._data[Wamit.Properties.BODY_POINTS], 
                                    return_velocity=return_velocity, 
                                    return_acceleration=return_acceleration)
            if relative:
                # evaluate the incident wave motion RAOs
                wave = Wamit.compute_incident_wave(self.periods, self.directions, 
                                        self._data[Wamit.Properties.BODY_POINTS],
                                        return_velocity=return_velocity, return_acceleration=return_acceleration)
                X -= wave

            if len(self.registered_body_points) == 1:
                return np.expand_dims(np.squeeze(X[:, ix, jx]), axis=0)
            else: return np.squeeze(X[:, ix, jx])
        else:
            X = self._data[Wamit.Properties.RAOS]
            #print("here", ij, X[ij].shape)
            jw = 1j*(2*np.pi/self.periods)
            factor = jw if return_velocity else jw**2 if return_acceleration else 1            
            if relative:
                # evaluate the incident wave motion RAOs
                wave = Wamit.compute_incident_wave(self.periods, self.directions, 
                                        np.expand_dims(np.r_[0,0,0], axis=0), # origin
                                        return_velocity=return_velocity, return_acceleration=return_acceleration)
                wave = np.squeeze(wave) # only xyz components, so lets pad for other modes to make general
                wave = np.vstack([wave, np.zeros(wave.shape)])
                #print("wave shape: ", wave.shape)
            return np.squeeze(X[ij]*factor - wave[ij]) if relative else np.squeeze(X[ij]*factor)


    def get_pressures(self, direction, ulen=1):
        """
        """
        # Make assertions
        assert direction in self.directions, "direction not computed, direction interpolation not implemented"    
        pressure = self._data[Wamit.Properties.BODY_PRESSURE_TRANSFER_FUNCTIONS]
        p_dif = pressure["diffraction"]
        p_rad = pressure["radiation"]
        ix = np.nonzero(self.directions == direction)
        p_dif = p_dif[ix,:,:]
        return np.squeeze(p_dif), p_rad
        

    def compute_std_deviations(self, Sxx, fz, mode=None, direction=None, 
        return_at_body_points=False, return_velocity=False, return_acceleration=False, 
        relative=False):
        """
            Returns the standard deviation of response in a given sea spectrum Sxx(fz),
            where fz is in Hzs. This function uses pre-existing RAO data; to use this 
            function either solve_EOM or solve_stochastic must have been run. 
            The user can request:
                - a specific mode of motion ... all modes of motion returned as default
                - a specific wave direction ... all directions return as default
                - acceleration or velocity to be return instead of the motion raos
            If return_at_body_points=True, the values are returned at the body point locations 
            The body point locations are registered with register_body_points function.
            if returning at body point locations, only translation modes 0,1,2 available
        """
        
        X = self.get_raos(mode=mode, direction=direction, return_at_body_points=return_at_body_points,
                return_velocity=return_velocity, return_acceleration=return_acceleration, relative=relative)

        if X.ndim == 1:
            H = interpc(fz, 1/self.periods, X)
            return np.trapz(Sxx*np.abs(H)**2, fz)**0.5
        else:
            original_shape = X.shape
            size = int(np.product(original_shape))
            nfreqs = original_shape[-1] # also len(self.periods)
            X = X.reshape((size//nfreqs, nfreqs))
            stds = np.zeros(size//nfreqs)
            for i, Xi in enumerate(X):
                H = interpc(fz, 1/self.periods, Xi)
                stds[i] = np.trapz(Sxx*np.abs(H)**2, fz)**0.5
            return stds.reshape(original_shape[:-1])


    def compute_upcrossing_periods(self, Sxx, fz, mode=None, direction=None, 
        return_at_body_points=False, return_velocity=False, return_acceleration=False, 
        relative=False):
        """
            Returns the standard deviation of response in a given sea spectrum Sxx(fz),
            where fz is in Hzs. This function uses pre-existing RAO data; to use this 
            function either solve_EOM or solve_stochastic must have been run. 
            The user can request:
                - a specific mode of motion ... all modes of motion returned as default
                - a specific wave direction ... all directions return as default
                - acceleration or velocity to be return instead of the motion raos
            If return_at_body_points=True, the values are returned at the body point locations 
            The body point locations are registered with register_body_points function.
            if returning at body point locations, only translation modes 0,1,2 available
        """
        
        X = self.get_raos(mode=mode, direction=direction, return_at_body_points=return_at_body_points,
                return_velocity=return_velocity, return_acceleration=return_acceleration, relative=relative)

        if X.ndim == 1:
            H = interpc(fz, 1/self.periods, X)
            m0 = np.trapz(Sxx*np.abs(H)**2, fz)
            m2 = np.trapz(Sxx*np.abs(H)**2*fz**2, fz)
            return np.sqrt(self._suppressed_division(m0, m2))
        else:
            original_shape = X.shape
            size = int(np.product(original_shape))
            nfreqs = original_shape[-1] # also len(self.periods)
            X = X.reshape((size//nfreqs, nfreqs))
            Tz = np.zeros(size//nfreqs)
            for i, Xi in enumerate(X):
                H = interpc(fz, 1/self.periods, Xi)
                m0 = np.trapz(Sxx*np.abs(H)**2, fz)
                m2 = np.trapz(Sxx*np.abs(H)**2*fz**2, fz)
                Tz[i] = np.sqrt(self._suppressed_division(m0, m2))
            return Tz.reshape(original_shape[:-1])


    def compute_statistics(self, Sxx, fz, mode=None, direction=None, 
        return_at_body_points=False, return_velocity=False, return_acceleration=False, 
        relative=False, duration_of_seastate=3, user_specified_fractile=0.9):
        """
            Returns the standard deviation of response in a given sea spectrum Sxx(fz),
            where fz is in Hzs. This function uses pre-existing RAO data; to use this 
            function either solve_EOM or solve_stochastic must have been run. 
            The user can request:
                - a specific mode of motion ... all modes of motion returned as default
                - a specific wave direction ... all directions return as default
                - acceleration or velocity to be return instead of the motion raos
            If return_at_body_points=True, the values are returned at the body point locations 
            The body point locations are registered with register_body_points function.
            if returning at body point locations, only translation modes 0,1,2 available
        """
        
        X = self.get_raos(mode=mode, direction=direction, return_at_body_points=return_at_body_points,
                return_velocity=return_velocity, return_acceleration=return_acceleration, relative=relative)

        D  = duration_of_seastate*3600 # seconds

        #print("RAO stats shape: ", X.shape)

        if X.ndim == 1:
            H = interpc(fz, 1/self.periods, X)
            m0 = np.trapz(Sxx*np.abs(H)**2, fz)
            m2 = np.trapz(Sxx*np.abs(H)**2*fz**2, fz)
            Tz = np.sqrt(self._suppressed_division(m0, m2))
            N  = D/Tz
            #alpha = 1 - user_specified_fractile
            #user_extreme = np.sqrt(-2*m0*np.log(1.-(1.-alpha)**(1./N)))
            user_extreme = np.sqrt(-2*m0*np.log(1.-user_specified_fractile**(1./N)))
            mpm_extreme =  np.sqrt(2*m0*np.log(N))
            return np.sqrt(m0), Tz, mpm_extreme, user_extreme
        else:
            original_shape = X.shape
            size = int(np.product(original_shape))
            nfreqs = original_shape[-1] # also len(self.periods)
            X = X.reshape((size//nfreqs, nfreqs))
            tzs = np.zeros(size//nfreqs)
            stds = np.zeros(size//nfreqs)
            mpm_extremes = np.zeros(size//nfreqs)
            user_extremes = np.zeros(size//nfreqs)
            for i, Xi in enumerate(X):
                H = interpc(fz, 1/self.periods, Xi)
                m0 = np.trapz(Sxx*np.abs(H)**2, fz)
                m2 = np.trapz(Sxx*np.abs(H)**2*fz**2, fz)
                tzs[i] = np.sqrt(self._suppressed_division(m0, m2))
                N  = D/tzs[i]
                user_extremes[i] = np.sqrt(-2*m0*np.log(1.-user_specified_fractile**(1./N)))
                mpm_extremes[i] =  np.sqrt(2*m0*np.log(N))
                stds[i] = np.sqrt(m0)
            return np.array([stds.reshape(original_shape[:-1]), 
                    tzs.reshape(original_shape[:-1]),
                    mpm_extremes.reshape(original_shape[:-1]),
                    user_extremes.reshape(original_shape[:-1])])


    def _suppressed_division(self, nominator, demoninator):
        import warnings
        warnings.filterwarnings("ignore")
        return np.nan_to_num(nominator/demoninator)


    def _compute_natural_periods(self, verbose=False):
        if self._data[Wamit.Properties.STIFFNESS_HYDROGRAV] is None:
            raise Exception(f"Hydro stiffness not read. No {self.fname}.out file present")

        natural_periods = np.zeros(6) # storage for natural periods
        critical_damping = np.zeros(6) # storage for critical damping
        M = self._data[Wamit.Properties.MASS]   
        AM = self._data[Wamit.Properties.ADDED_MASS]   
        C = self._data[Wamit.Properties.STIFFNESS_HYDROGRAV]   
        Xg,Yg,Zg = self._data[Wamit.Properties.MASS_CENTER]
        w = 2*np.pi/self.periods
        
        
        # Formula for natural period relates to a COG centered system

        # Subtract of Steiner term to get inertia to COG
        for i in [3,4]: M[i,i] -= M[0,0]*Zg**2

        # TODO: How to adjust for added mass (rotation FS => COG)

        # Natural frequency in heave, roll and pitch
        for i in [2,3,4]:
            print(i, C[i,i], M[i,i], 2*np.pi*np.sqrt(M[i,i]/(C[i,i])))
            res = opt.minimize(
                fun=lambda wn: abs(wn - np.sqrt(C[i,i]/(M[i,i] + np.interp(wn,w,AM[i,i])))),
                x0=np.sqrt(C[i,i]/M[i,i]))

        #for i in [2,3,4]:
        #    print(i, C[i,i], M[i,i], 2*np.pi*np.sqrt(M[i,i]/(C[i,i])))
        #    res = opt.minimize(
        #        fun=lambda wn: abs(wn - np.sqrt(C[i,i]/(M[i,i]))),
        #        x0=np.sqrt(C[i,i]/M[i,i]))
            natural_periods[i] = 2*np.pi/res.x
            critical_damping[i] = 2*res.x*(M[i,i])
            AMii = np.interp(res.x,w,AM[i,i]) 
            print(AMii, AMii/M[i,i])

        self._data[Wamit.Properties.NATURAL_PERIODS] = natural_periods
        self._data[Wamit.Properties.CRITICAL_DAMPING] = critical_damping 
        
        if verbose:
            for i, dof in zip([2,3,4],"heave roll pitch".split()):
                wn = 2*np.pi/natural_periods[i]
                Tn = 2*np.pi/np.sqrt(C[i,i]/(M[i,i] + np.interp(wn,w,AM[i,i])))
                print(f"Computed natural periods in {dof}: {natural_periods[i]:.1f} s " +
                      f"(Check: {Tn:.1f} s)")


    def add_slender_element(self, x1, x2, xref, Cl, Cq, Ca, N):
        se = Wamit.SlenderElement(x1, x2, xref, Cl, Cq, Ca, N)
        if self._data[Wamit.Properties.SLENDER_ELEMENTS] is None:
            self._data[Wamit.Properties.SLENDER_ELEMENTS] = [se]
        else:
            self._data[Wamit.Properties.SLENDER_ELEMENTS] += [se]

    def _evaluate_slender_element_wave_excitation(self, iper, ibeta, amp=1.0, vstd=None, 
                                                    g=9.80665, verbose=False):
        """
            vstd relates to the 3d space (there is no vstd for the roll in this setup)
        """
        Fv = np.zeros(3, np.complex)
        Mv = np.zeros(3, np.complex)

        period = self.periods[iper]
        beta = self.directions[ibeta]
        omega = 2*np.pi/period
        k = omega**2/g

        
        for ise, se in enumerate(self._data[Wamit.Properties.SLENDER_ELEMENTS]):

            if vstd is not None:
                B = np.array([se._Cq*np.sqrt(8/np.pi)*vstd]).T # column vector (3,1)
            else:
                B = np.array([se._Cq*8/3/np.pi*amp*(2*np.pi/period)]).T # column vector (3,1)
                #B = se._Cq*8/3/np.pi*amp*(2*np.pi/period) # surely this needs commenting out 
            
            #print(f"Contribution from Slender Element {ise+1}")
            e = se.local_basis 
            points = se.points
            dl = se._dl           

            for ipoint, point in enumerate(points):       
                x,y,z = point
                r = np.array( # cross product matrix
                    [
                        [ 0, -z,  y],
                        [ z,  0, -x],
                        [-y,  x,  0]
                    ]
                )

                eta = np.exp(-1j*(k*x*np.cos(beta) + k*y*np.sin(beta))) # phase shift to x
                u  = np.r_[     # Wave velocity at the point
                    omega*np.cos(beta)*np.exp(k*z)*eta,
                    omega*np.sin(beta)*np.exp(k*z)*eta,
                    1j*omega*np.exp(k*z)*eta]
                print(f"period: {period}, u: {u}")
                u = -u  # for long wave expect it to be approx Fv and u to be ~ 0 - |F|*1j 
                dF = e.T@(B*dl*e)@u
                dM = np.cross(point, dF) #r@Fv
                Fv += dF
                Mv += dM


                print(f"Point: {point}")
                print(f"Fv contribution: {dF}")
                print(f"Mv contribution: {dM}")
            
        F = np.r_[Fv,Mv]
        print(f"Viscous Wave Force:\n{F}")
        print(f"Wave heading: {beta}")
        print(f"Wave period: {period}")
        sys.exit()
        return F


    def _evaluate_slender_element_damping(self, iper, ibeta, amp=1.0, vstd=None):
        """ Direction independent at the moment, and if vstd used, it is also
        period independent. So if vstd is used then the damping matrix is constant
        for all directions and periods which is desirable as a damping matrix is
        direction independent (direction is built into the rows and columns)
        """
        BV = np.zeros((6,6))
        for ise, se in enumerate(self._data[Wamit.Properties.SLENDER_ELEMENTS]):
            #print(f"Contibution from Slender Element {ise+1}")
            # u_I and u-B have dimensions (Np, 3, Nbeta, Nfreq)
            #u_I = Wamit.compute_incident_wave(self.periods, self.directions, se.points) 
            #u_B = self.transform_rao(se.points, return_velocity=True)
            e = se.local_basis 
            points = se.points
            dl = se._dl           
            # simplify matrix operations during initial implementation
            # by removing periods and directions from the matrix system
            period = self.periods[iper]
            beta = self.directions[ibeta]
            if vstd is not None:
                B = np.array([se._Cq*np.sqrt(8/np.pi)*vstd]).T # column vector (3,1)
            else:
                B = np.array([se._Cq*8/3/np.pi*amp*(2*np.pi/period)]).T # column vector (3,1)
            I = np.eye(3)
            O = np.zeros((3,3))
            
            for ipoint, point in enumerate(points):       
                x,y,z = point

                # Need to be careful with the application or r
                # For Force to Moment we have r ^ F
                # However for rotation to linear velocity we have theta ^ r
                r = np.array( # cross product matrix
                    [
                        [ 0, -z,  y],
                        [ z,  0, -x],
                        [-y,  x,  0]
                    ]
                )


                #print(f"local basis e:\n {e}")
                #print(f"Damping coeffs B:\n {B}")
                #print(f"Length of segment dl: {dl}")             
                #print(f"local basis B*dl*e:\n {B*dl*e}")
                #print(f"B.shape: {B.shape}")
                
                E = (B*dl*e)
                U1 = I # translation
                U2 = -r # rotation contribution (need to make negative as u = theta ^ r not r ^ theta)


                # Why bother with this transformation??? 
                #A11 = (U1.T@E.T).T  # top left block  => dF local contribution due to translations
                #A12 = (U2.T@E.T).T  # top right block => dF local contribution due to rotations
                A11 = E@U1 # top left block  => dF local contribution due to translations
                A12 = E@U2 # top right block => dF local contribution due to rotations


                #print(f"A11 (local):\n{A11}")
                #print(f"A12 (local):\n{A12}")

                A11 = e.T@A11  # top left block  => dF global contribution due to translations
                A12 = e.T@A12  # top right block => dF global contribution due to rotations

                #print(f"A11 (global):\n{A11}")
                #print(f"A12 (global):\n{A12}")
                
                # Not quite mastered this (needed -ve to make positive)
                A21 = r@A11  # top left block  => dM global contribution due to translations
                A22 = r@A12  # top right block => dM global contribution due to rotations

                #print(f"A21 (global):\n{A21}")
                #print(f"A22 (global):\n{A22}")

                A = np.block([[ A11, A12],[A21,  A22]])
                #print(f"block damping matrix contribution, A:\n {A}")
                BV += A

        #print(f"Summed, damping matrix:\n {BV}")
        #sys.exit()
        return BV
           

    def transform_rao(self, body_pts, return_velocity=False, return_acceleration=False):
        """ Returns an rao transformed to the body point, pt = (x,y,z)
            raos have shape (6, nBeta, nPeriods)
            body_pts (Np, 3)
            linear_xyz (Np, 3, nBeta, nPeriod)
        """
        X = self.wave_to_motion_tfs
        assert X is not None, "Need to solve the solution first using solve_EOM or solve_stochastic!"
        single_point = True if body_pts.ndim == 1 else False
        npoints = 1 if single_point else len(body_pts)
        linear_xyz = np.zeros((npoints, *X[3:].shape), np.complex)
        if single_point:
            linear_xyz[0] = X[:3] + np.cross(X[3:], body_pts, axisa=0, axisc=0) 
        else:
            for ipt, pt in enumerate(body_pts):
                linear_xyz[ipt] = X[:3] + np.cross(X[3:], pt, axisa=0, axisc=0) 
        jw = 1j*(2*np.pi/self.periods)
        if return_velocity: return linear_xyz*jw
        elif return_acceleration: return linear_xyz*(jw)**2
        else: return linear_xyz

    def _compute_BQE(self, Sxx, fz):
        X = self.wave_to_motion_tfs
        if X is None: 
            self.solve_EOM(amp=1.0) # make an initial (recently changed to facilitate chaining)
            X = self.wave_to_motion_tfs 
        BQE = self._data[Wamit.Properties.LINEARIZED_QUADRATIC_DAMPING_EXTERNAL]
        BQ = self._data[Wamit.Properties.QUADRATIC_DAMPING_EXTERNAL]
        # compute the standard deviation of response for each direction
        for imode, Xi in enumerate(X): # for each response mode and ... 
            for ibeta, beta in enumerate(self.directions): # .. each direction
                # standard deviations of response
                H = interpc(fz, 1/self.periods, np.squeeze(Xi[ibeta]))
                V = np.trapz(Sxx*np.abs(1j*(2*np.pi*fz)*H)**2, fz)**0.5 # Std dev
                BQE[ibeta,imode,imode] = (8/np.pi)**0.5 * V * BQ[imode, imode] # No need to store V = BQE*sqrt(pi/8)
        self._data[Wamit.Properties.LINEARIZED_QUADRATIC_DAMPING_EXTERNAL] = BQE
        return BQE*1.0 # unsure about python references


    def solve_EOM(self, amp=1.0, vstd=None, slender_on=True, print_BSUM=False):
        "Solves the equation of motion"
        import matplotlib.pyplot as plt

        np.set_printoptions(precision=2)
        M = self._data[Wamit.Properties.MASS]
        A = self._data[Wamit.Properties.ADDED_MASS]
        AE = self._data[Wamit.Properties.ADDED_MASS_ZERO_EXTERNAL]
        B = self._data[Wamit.Properties.DAMPING]
        BE = self._data[Wamit.Properties.DAMPING_EXTERNAL]
        C = self._data[Wamit.Properties.STIFFNESS_HYDROGRAV]
        CE = self._data[Wamit.Properties.STIFFNESS_EXTERNAL]
        F = self._data[Wamit.Properties.EXCITE_DIFF]
        X = self._data[Wamit.Properties.RAOS]
        BQE = self._data[Wamit.Properties.LINEARIZED_QUADRATIC_DAMPING_EXTERNAL]

        # Solve for all direction 0, all periods
        X_ = np.zeros(X.shape, np.complex)
        
        for ibeta, beta in enumerate(self.directions):

            #print(f"Heading {beta:.1f}:\nBE={BE}\nBQE={BQE[ibeta]}")
            for iper, period in enumerate(self.periods):
                w = 2*np.pi/period

                # If slender elements are present compute 
                if self._data[Wamit.Properties.SLENDER_ELEMENTS] is not None and slender_on:
                    BV = self._evaluate_slender_element_damping(iper, ibeta, amp, vstd=vstd)
                    FV = self._evaluate_slender_element_wave_excitation(iper, ibeta, amp, vstd=vstd)
                    #print(f"Period, Heading: {period, beta}")
                    #print(f"Viscous damping\n: {BV}")
                    #print(f"Viscous excitation\n: {FV}")
                    #sys.exit()   

                lhs = -w**2*(M+A[:,:,iper]+AE)+1j*w*(B[:,:,iper]+BE+BQE[ibeta])+(C+CE)
                rhs = F[:,ibeta,iper]*1.0

                # TODO: Add viscous wave excitation to rhs (initial check?
                #g = 9.80665
                #z = -22
                #x, y = 0, 0
                #k = w**2/g
                #eta = np.exp(-1j*(k*x*np.cos(beta) + k*y*np.sin(beta))) # phase shift to x
                #u  = np.r_[w*np.cos(beta)*np.exp(k*z)*eta,
                #           w*np.sin(beta)*np.exp(k*z)*eta,
                #           1j*w*np.exp(k*z)*eta, 0, 0, 0]
                #print(rhs)
                #rhs[2] = rhs[2] + BQE[ibeta,2,2]*u[2]
                #rhs[2] = rhs[2] + (BQE[ibeta,2,2]*1j*w*np.exp(k*z))

                if self._data[Wamit.Properties.SLENDER_ELEMENTS] is not None and slender_on:
                    rhs += FV # getting heave excitation effect due to heave pitch damping 
                    lhs += 1j*w*BV

                #x = np.linalg.solve(lhs, rhs)
                X_[:,ibeta,iper] = np.linalg.solve(lhs, rhs)

        # Update internals (RAOs and BQE)
        self._data[Wamit.Properties.RAOS] = X_
        #return X_
        return self # to facilitate chaining

    def solve_stochastic(self, Sxx, fz, verbose_heading=None):
        tol = 1E-7
        first_iteration = True
        factors = np.r_[1,1,1,180/np.pi,180/np.pi,180/np.pi]
        if verbose_heading is not None:
            BQdiag = np.diag(self._data[Wamit.Properties.QUADRATIC_DAMPING_EXTERNAL])
            print(BQdiag)

        while True:
            BQE_old = self._compute_BQE(Sxx, fz) if first_iteration else BQE_new
            #if verbose_heading is not None:
            #    tmp = np.diag(BQE_old[verbose_heading])*(np.pi/8)**0.5
            #    print(np.where(BQdiag>0, tmp/BQdiag, 0)*factors)
            self.solve_EOM() # solve the equations
            BQE_new = self._compute_BQE(Sxx, fz)                
            error = np.sum(np.abs(BQE_old-BQE_new))
            if verbose_heading is not None:
                print(f"Solving Stochastically: Current error {error:.10f}")
                print(np.diag(BQE_old[verbose_heading]))
            if error < tol: break   
            first_iteration = False 
        if verbose_heading is not None:
                tmp = np.diag(BQE_new[verbose_heading])*(np.pi/8)**0.5
                print([tmp[i]/BQdiag[i]*factors[i] if BQdiag[i]!=0 else 0 for i in range(6)])

        return self        


    def _update_retardation_functions(self):
        self._data[Wamit.Properties.RETARDATION_FUNCTIONS] = \
            Wamit.compute_retardation_functions(
                self._data[Wamit.Properties.PERIODS],
                self._data[Wamit.Properties.DAMPING], 
                dt=0.5, tmax=100)

    ###  --------- PROPERTY SECTION ----------  ####

    @property
    def periods(self): return self._data[Wamit.Properties.PERIODS]

    @property
    def directions(self): return self._data[Wamit.Properties.DIRECTIONS]

    @property
    def natural_periods(self): return self._data[Wamit.Properties.NATURAL_PERIODS]

    @property
    def critical_damping(self): return self._data[Wamit.Properties.CRITICAL_DAMPING]

    @property
    def retardation_functions(self): return self._data[Wamit.Properties.RETARDATION_FUNCTIONS]

    @property
    def linear_external_damping(self): return self._data[Wamit.Properties.DAMPING_EXTERNAL]

    @property
    def linearized_quadratic_damping(self): return self._data[Wamit.Properties.LINEARIZED_QUADRATIC_DAMPING_EXTERNAL]

    @property
    def linear_external_stiffness(self): return self._data[Wamit.Properties.STIFFNESS_EXTERNAL]

    @property
    def quadratic_external_damping(self): return self._data[Wamit.Properties.QUADRATIC_DAMPING_EXTERNAL]

    @property
    def external_added_mass(self): return self._data[Wamit.Properties.ADDED_MASS_ZERO_EXTERNAL]

    @property
    def wave_to_motion_tfs(self): return self._data[Wamit.Properties.RAOS]

    @property
    def mass_matrix(self): return self._data[Wamit.Properties.MASS]

    @property
    def body_panels_info(self): return self._data[Wamit.Properties.BODY_PANELS]

    @property
    def body_pressure_tfs(self): return self._data[Wamit.Properties.BODY_PRESSURE_TRANSFER_FUNCTIONS]


    ###  --------- STATIC METHODS ----------  ####

    @staticmethod
    def compute_retardation_functions(periods, damping_matrix, dt=0.5, tmax=100):
        w = 2*np.pi/periods
        wi = np.linspace(1E-12, w.max(), 1000)
        time = np.arange(0,tmax+dt/2,dt)
        rets = np.zeros((6,6,len(time))) # retardation fns 
        for i in range(6):
            for j in range(6):
                bi = np.interp(wi, w, damping_matrix[i,j,:]) 
                rets[i,j]= np.r_[[2/np.pi*np.trapz(bi*np.cos(wi*t), wi) for t in time]]
        return rets

    @staticmethod
    def read_hydrograv_stiffness(filename, ulen=1.0, density=1.025, g=9.80665):
        c = np.zeros((6,6))
        with open(filename) as fin:
            lines = fin.readlines()
            location = find_occurrences("gravitational", lines, specificOccurrenceWanted=1)
            c[2,2:5] = [float(value) for value in lines[location+1].split()[-3:]]
            c[3,3:]  = [float(value) for value in lines[location+2].split()[-3:]]
            c[4,4:]  = [float(value) for value in lines[location+3].split()[-2:]]
            c = c + c.T - np.diag(np.diag(c))
        i, j =  np.indices((6,6))
        k = i//4 + j//4 + 2
        c = c*density*g*ulen**k
        wamit = Record(f"Stiffness properties from {filename}")
        wamit.addattr(stiffness=c)
        return wamit


    @staticmethod
    def read_mass_matrix(filename):
        I, J, mass, damping, stiffness = loadtxt(filename, skip_header=12, transpose=True)
        mass, damping, stiffness = [arr.reshape((6,6)) for arr in [mass, damping, stiffness]]
        get_values = lambda string, lines: np.r_[[float(value) for value in 
            lines[find_occurrences(string, lines, specificOccurrenceWanted=1)].split()[-3:]]]

        with open(filename, "r") as fin:
            lines = fin.readlines()
            vols = get_values("Volumes", lines)
            cob = get_values("Center of Buoyancy", lines)
            cog = get_values("Center of Gravity", lines)

        wamit = Record(f"Mass properties from {filename}")
        wamit.addattr(mass=mass, damping=damping, stiffness=stiffness, cob=cob, cog=cog, vols=vols)
        return wamit

    @staticmethod
    def read_added_mass_and_damping(filename, ulen=1.0, density=1.025, frequency_ascending=False):
        """ Returns the dimensionalized added mass
        """
        periods = np.loadtxt(filename, usecols=(0,))
        periods = np.r_[sorted(set(periods))]
        nperiods = len(periods) - np.sum(periods <= 0)
        periods = periods[periods > 0]
        a0, ainf = np.zeros((2,6,6))
        added_mass = np.zeros((6, 6, nperiods))
        damping = np.zeros((6, 6, nperiods))
        with open(filename, 'r') as fin:
            for line in fin.readlines():
                vars = [float(var) for var in line.split()]
                # note that for periods 0 and -1 bij is dummy        
                (period, i, j, aij), bij = vars[:4], vars[-1] 
                i, j = int(i), int(j)
                k = i//4 + j//4 + 3
                aij = aij*density*ulen**k
                if period == 0:
                    a0[i-1, j-1] = aij
                elif period < 0:
                    ainf[i-1, j-1] = aij
                else:
                    bij = bij*density*ulen**k*(2*np.pi/period)
                    added_mass[i-1, j-1,
                               np.argmin(abs(periods-period))] = aij
                    damping[i-1, j-1,
                               np.argmin(abs(periods-period))] = bij
        if frequency_ascending:
            periods = periods[::-1]
            added_mass = added_mass[:,:,::-1]
            damping = damping[:,:,::-1]
        wamit = Record("periods from %s" % filename)
        wamit.addattr(periods=periods, added_mass=added_mass, damping=damping, ainf=ainf, a0=a0)
        return wamit

    @staticmethod
    def read_excitation_forces(filename, ulen=1.0, density=1.025, g=9.80665, frequency_ascending=False):
        # Format PER BETA I Mod(Xi) Pha(Xi) Re(Xi) Im(Xi)
        periods, directions, dofs, amp, phase, re, im =  loadtxt(filename, transpose=True)
        periods = np.r_[sorted(set(periods))]
        directions = np.r_[sorted(set(directions))]
        value = (re + 1j*im)*density*g*ulen**(1+dofs//4)
        dofs = sorted(set(dofs))
        value = np.einsum('lkj->jkl', value.reshape((len(periods), len(directions), len(dofs))))
        if frequency_ascending:
            periods = periods[::-1]
            value = value[:,:,::-1]
        tfs = Record(f'Excitation forces from {"Haskind Relations" if filename.endswith("2") else "Diffraction Potential"}')
        tfs.addattr(value=value, directions=directions, periods=periods)

        #print(filename)
        #if filename == "wamit.3":
        #    for iper, period in enumerate(periods):
        #        if period == 10:
        #            print(value[2,0,iper], density*g)
        #
        #    sys.exit()
        return tfs

    @staticmethod
    def read_raos(filename="wamit_.4", ulen=1.0, nbodies=1, frequency_ascending=False):
        """ Reads a wamit.4 file - nbodies not implemented"""
        periods, directions, dofs, amp, phase, re, im =  loadtxt(filename, transpose=True)
        periods = np.r_[sorted(set(periods))]
        directions = np.r_[sorted(set(directions))]
        value = (re + 1j*im)/ulen**(dofs//4)
        value = np.einsum('lkj->jkl', value.reshape((len(periods), len(directions), 6)))
        if frequency_ascending:
            periods = periods[::-1]
            value = value[:,:,::-1]
        tfs = Record(f'Wave to motion transfer function')
        tfs.addattr(value=value, directions=directions, periods=periods)
        return tfs

    @staticmethod
    def compute_wavenumber(w, h, g = 9.80665):
        """ Returns the wave number satisfying the first order linear dispersion relation w**2 = gktanh(kh)
        """
        from scipy.optimize import root_scalar
        # To relax requirement on input allow for both iterable and non-iterable inputs
        made_iterable = False
        if not hasattr(w,'__iter__'): 
            w = np.ones(1)*w # make iterable
            made_iterable = True

        k = np.zeros(len(w))
        for i, wi in enumerate(w):
            sol = root_scalar(lambda k_, h, w: w**2 - g*k_*np.tanh(k_*h), 
                                args=(h, wi), method='brentq', bracket=[0, 10])
            if not sol.converged: print(f"Period {2*np.pi/wi} is not converged.")
            k[i] = sol.root

        return k[0] if made_iterable else k

    @staticmethod
    def compute_incident_wave(periods, directions, fpts, depth=1000, g=9.80665, 
            return_velocity=False, return_acceleration=False):
        """ 
        Computes the incident wave (origin) to wave (field point) transfer function
        TODO: Investigate computation of shallow water depth dependency term
        WAMIT quantities are phased with respect to the incident wave elevation at X=Y=0 
        """
        from scipy.optimize import minimize
        import warnings
        warnings.filterwarnings("ignore")
        omega = 2*np.pi/periods
        k = Wamit.compute_wavenumber(omega, depth, g)
        kx = np.zeros((len(fpts), len(directions), len(periods)), np.complex)
        u = np.zeros((len(fpts), 3, len(directions), len(periods)), np.complex)
        # Evaluate the wave-to-wave elevation tf at the field points
        jw = 1j*omega
        factor = jw if return_acceleration else 1 if return_velocity else 1/jw # for position

        for ib, beta in enumerate(directions*np.pi/180):
            for ip, (x,y,z) in enumerate(fpts):
                kx[ip, ib] = np.exp(-1j*(k*x*np.cos(beta) + k*y*np.sin(beta))) # phase shift for xy
                #u[ip, ib] = np.cos(beta)*omega*np.cosh(k*(z+depth))/np.sinh(k*depth)*kx[ip, ib]
                #v[ip, ib] = np.sin(beta)*omega*np.cosh(k*(z+depth))/np.sinh(k*depth)*kx[ip, ib]
                #w[ip, ib] = 1j*omega*np.sinh(k*(z+depth))/np.sinh(k*depth)*kx[ip, ib]
                u[ip, 0, ib] = np.cos(beta)*omega*np.exp(k*z)*kx[ip, ib]*factor # horizontal is in phase with elevation
                u[ip, 1, ib] = np.sin(beta)*omega*np.exp(k*z)*kx[ip, ib]*factor # horizontal is in phase with elevation
                u[ip, 2, ib] = 1j*omega*np.exp(k*z)*kx[ip, ib]*factor           # vertical is -sin
        return u

    @staticmethod
    def read_body_pressure_tfs(filename="wamit.5p", nbodies=1):
        """ Reads a wamit.5p file - nbodies not implemented  - assumes INUMOPT5 = 1"""
        data = open(filename, "r").readlines()
        data = [list(map(float, line.split())) for line in data]
        data_rad = np.array([line for line in data if len(line)==15]).T
        data_dif = np.array([line for line in data if len(line)==6]).T
        wave_periods, directions, quadrant, pid = data_dif[:4]
        wave_periods = np.sort(np.r_[list(set(wave_periods))])
        directions = np.sort(np.r_[list(set(directions))])
        nf, nd = len(wave_periods), len(directions)
        npanels = int(max(pid)*max(quadrant))
        re_rad, im_rad = data_rad[3::2], data_rad[4::2]
        re_dif, im_dif = data_dif[4], data_dif[5]
        h_rad = re_rad + 1j * im_rad
        h_dif = re_dif + 1j * im_dif
        h_rad = np.einsum('ijk->ijk', h_rad.reshape((6, nf, npanels))) # leave unchanged
        h_dif = np.einsum('kjl->jkl', h_dif.reshape((nf, nd, npanels)))

        # reverse periods to suit SIMO and aid integrations using w
        wave_periods = wave_periods[::-1]
        h_dif = np.flip(h_dif, axis=1) # flip frequency axis (index 1 after einsum)
        h_rad = np.flip(h_rad, axis=1) # flip frequency axis

        pres = Record("Pressure on body from %s" % filename)
        pres.directions = directions
        pres.frequencies = 2 * np.pi / wave_periods
        pres.periods = wave_periods
        pres.h_rad = h_rad
        pres.h_dif = h_dif

        for ibody in range(nbodies):
            for idof, name in enumerate("surge sway heave roll pitch yaw".split()):
                pres.setattr(name, h_rad[idof])

        return pres

    @staticmethod
    def read_wamit_normals(filename="wamit.pnl", nbodies=1):
        xc, yc, zc, area, nx, ny, nz, rnx, rny, rnz = np.loadtxt(filename, usecols=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11)).T
        geom = Record("Areas and normals from %s" % filename)
        geom.area = area
        geom.xc  = xc
        geom.yc  = yc
        geom.zc  = zc
        geom.nx  = nx 
        geom.ny  = ny 
        geom.nz  = nz 
        geom.rnx = rnx
        geom.rny = rny
        geom.rnz = rnz
        geom.npanels = len(xc)
        return geom
    

############ TO BE DEPRECATED BELOW THIS LINE #############


def read_simo_raos(filename, bodyname=None):
    """ If the file contains more than one body, then you need to identify the body"""

    # Create record for storage
    rao = Record("rao from %s" % filename)

    # alias the data appropriately
    lines = open(filename, 'r').readlines()

    # strip whitespace
    lines = list([line for line in lines
                  if not line.strip().startswith("'")])

    # find occurances of wave drift (assume none in text)
    loc = [i+1 for i, l in enumerate(lines)
           if 'motion' in l.lower() and 'transfer' in l.lower()]

    # read number of frequencies
    nd, nf = map(int, lines[loc[0]+2].split()[:2])

    # read frequencies and directions
    rao.directions = \
        np.r_[list(map(float, [l.split()[1]
                               for l in lines[loc[1]:loc[1]+nd]]))]
    rao.frequencies = \
        np.r_[list(map(float, [l.split()[1]
                               for l in lines[loc[2]:loc[2]+nf]]))]

    # read RAOs forces
    for i in loc[3:]:
        data = np.r_[[float(l.split()[2]) *
                      np.exp(1j*float(l.split()[3])*np.pi/180.)
                      for l in lines[i:i+nd*nf]]]
        data = data.reshape((nd, nf))
        if 'surge' in lines[i-1].lower():
            rao.surge = data
        elif 'sway' in lines[i-1].lower():
            rao.sway = data
        elif 'heave' in lines[i-1].lower():
            rao.heave = data
        elif 'roll' in lines[i-1].lower():
            rao.roll = data
        elif 'pitch' in lines[i-1].lower():
            rao.pitch = data
        elif 'yaw' in lines[i-1].lower():
            rao.yaw = data

    return rao


def read_wamit_raos(filename="wamit_.4", nbodies=1):
    """ Reads a wamit.4 file - nbodies not implemented"""
    wave_periods, directions, dof, amp, phase, re, im = np.loadtxt(filename).T
    wave_periods = np.sort(np.r_[list(set(wave_periods))])
    directions = np.sort(np.r_[list(set(directions))])
    nf, nd = len(wave_periods), len(directions)
    re = np.einsum('lkj->jkl', re.reshape((nf, nd, 6)))
    im = np.einsum('lkj->jkl', im.reshape((nf, nd, 6)))
    h = re + 1j * im

    # reverse periods to suit SIMO
    wave_periods = wave_periods[::-1]
    h = h[:, :, ::-1]

    rao = Record("RAOs from %s" % filename)
    rao.directions = directions
    rao.frequencies = 2 * np.pi / wave_periods
    rao.periods = wave_periods
    rao.h = h

    for ibody in range(nbodies):
        for idof, name in enumerate("surge sway heave roll pitch yaw".split()):
            rao.setattr(name, h[idof, :, :].reshape((nd, nf)))

    return rao


def read_wamit_mean_drift(filename="wamit_.8", nbodies=1, rho=1.025, g=9.80665, momentum=True):
    """ Reads a wamit.8 file - nbodies not implemented"""
    wave_periods, directions, direction2, dof, amp, phase, re, im = np.loadtxt(filename).T
    wave_periods = np.sort(np.r_[list(set(wave_periods))])
    directions = np.sort(np.r_[list(set(directions))])
    nf, nd = len(wave_periods), len(directions)
    re = np.einsum('lkj->jkl', re.reshape((nf, nd, 3 if momentum else 9)))
    im = np.einsum('lkj->jkl', im.reshape((nf, nd, 3 if momentum else 9)))
    h = re + 1j * im
    # reverse periods to suit SIMO
    wave_periods = wave_periods[::-1]
    h = h[:, :, ::-1]*rho*g
    # create record for export
    wdrift = Record("Wave drift (momentum) from %s" % filename)
    wdrift.directions = directions
    wdrift.frequencies = 2 * np.pi / wave_periods
    wdrift.periods = wave_periods
    wdrift.h = h
    # the last 3 in the case of pressure are relative the moving origin as opposed to mean position
    names = "surge sway yaw" if momentum else "surge sway heave roll pitch yaw roll2 pitch2 yaw2"
    for ibody in range(nbodies):
        for idof, name in enumerate(names.split()):
            wdrift.setattr(name, h[idof, :, :].reshape((nd, nf)))
    return wdrift



def read_wave_elevation_tfs(filename="wamit_.6p"):
    wave_periods, directions, fpts, amp, phase, re, im = np.loadtxt(filename).T
    wave_periods = np.sort(np.r_[list(set(wave_periods))])
    directions = np.sort(np.r_[list(set(directions))])
    fpts = np.sort(np.r_[list(set(fpts))])
    nf, nd, nfpts = len(wave_periods), len(directions), len(fpts)
    re = np.einsum('lkj->jkl', re.reshape((nf, nd, nfpts)))
    im = np.einsum('lkj->jkl', im.reshape((nf, nd, nfpts)))
    h = re + 1j * im

    # reverse periods to suit SIMO
    wave_periods = wave_periods[::-1]
    h = h[:, :, ::-1]

    wave = Record("Wave elevation from %s" % filename)
    wave.directions = directions
    wave.frequencies = 2 * np.pi / wave_periods
    wave.periods = wave_periods
    wave.elev = h

    return wave


def export_raos_to_simo(raos, body_name="body"):
    from ..administration.tools import sed
    sysfile = "sys-raos.dat"
    infile = sysfile + "0"
    outfile = sysfile
    beta = raos.directions
    w = raos.frequencies

    xxxdirs = ''.join(['\n%d  %.1f' % (i+1, d) for i, d in enumerate(beta)])
    xxxfreqs = ''.join(["\n %6d   %f" % (i+1, f) for i, f in enumerate(w)])
    sed(infile, {"xxxndirs": len(beta), "xxxnfreq": len(w)}, outfile)

    infile = outfile
    sed(infile, {"xxxdirs": xxxdirs, "xxxfreqs": xxxfreqs}, outfile)
    for idof, name in enumerate("surge sway heave roll pitch yaw".split()):
        L = []
        for ihead in range(len(beta)):
            for ifreq in range(len(w)):
                L.append('\n %6d %6d %12.3e %12.3e' % (
                    ihead + 1, ifreq + 1,
                    np.abs(raos.h[idof, ihead, ifreq]),
                    np.angle(raos.h[idof, ihead, ifreq])*180./np.pi))

        sed(infile, {"xxx%sRAOs" % name: ''.join(L)}, outfile)
        sed(infile, {"xxxBODY": body_name}, outfile)
    try:
        os.remove("sys-%s.dat" % body_name)
    except:
        pass
    os.rename("sys-raos.dat", "sys-%s.dat" % body_name)


def read_added_mass(filename="wamit_.1", ulen=1.0, density=1.025):
    """ Returns the dimensionalized added mass
    """
    data = np.loadtxt(filename, usecols=(0, 1, 2, 3))
    period, I, J, added_mass = data.T
    # period = set(period)  # tmp to remove 0 and -1
    # period.remove(0)   # tmp to remove 0 and -1
    # period.remove(-1)  # tmp to remove 0 and -1
    periods = np.r_[sorted(set(period))]
    added_mass = np.zeros((6, 6, len(periods)))
    for row in data:
        period, i, j, aij = row
        if period in [-1, 0]:
            continue
        else:
            added_mass[int(i-1), int(j-1),
                       np.argmin(abs(periods-period))] = aij*density

    wamit = Record("periods from %s" % filename)
    wamit.periods = periods
    wamit.added_mass = added_mass
    return wamit


def read_added_mass_and_damping(filename="wamit_.1", ulen=1.0, density=1.025):
    """ Returns the dimensionalized added mass
    """
    periods = np.loadtxt(filename, usecols=(0,))
    periods = np.r_[sorted(set(periods))]
    nperiods = len(periods) - np.sum(periods <= 0)
    periods = periods[periods > 0]
    a0, ainf = np.zeros((2,6,6))
    added_mass = np.zeros((6, 6, nperiods))
    damping = np.zeros((6, 6, nperiods))
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            vars = [float(var) for var in line.split()]
            # note that for periods 0 and -1 bij is dummy        
            (period, i, j, aij), bij = vars[:4], vars[-1] 
            i, j = int(i), int(j)
            k = i//4 + j//4 + 3
            aij = aij*density*ulen**k
            bij = bij*density*ulen**k
            if period == 0:
                a0[i-1, j-1] = aij
            elif period < 0:
                ainf[i-1, j-1] = aij
            else:
                added_mass[i-1, j-1,
                           np.argmin(abs(periods-period))] = aij
                damping[i-1, j-1,
                           np.argmin(abs(periods-period))] = bij

    wamit = Record("periods from %s" % filename)
    wamit.addattr(periods=periods, added_mass=added_mass, damping=damping, ainf=ainf, a0=a0)
    return wamit


def read_motion_tfs_not_used(filename="wamit_.4"):
    # laod and unpack data
    data = np.loadtxt(filename)
    period, direction, dof, amp, phase, re, im = data.T
    # reshape arrays
    periods = sorted(set(period))
    directions = sorted(set(direction))
    dofs = sorted(set(dof))
    mats = [period, direction, dof, amp, phase, re, im]  # pack
    for i in range(len(mats)):
        mats[i] = mats[i].reshape(len(periods), len(directions), len(dofs))
    period, direction, dof, amp, phase, re, im = mats  # unpack
    # package for returning
    tfs = Record("motion_tfs")
    tfs.addattr(amp=amp, phase=phase, re=re, im=im,
                dirs=direction, pers=period,
                directions=directions, periods=periods)
    # if direction and periods not order use einsum to reorder
    return tfs


def read_wave_elevation_tfs_not_used(filename="wamit_.6p"):
    data = np.loadtxt(filename)
    period, direction, fpt, amp, phase, re, im = data.T
    periods = sorted(set(period))
    directions = sorted(set(direction))
    fpts = sorted(set(fpt))
    mats = [period, direction, fpt, amp, phase, re, im]  # pack
    for i in range(len(mats)):
        mats[i] = mats[i].reshape(len(periods), len(directions), len(fpts))
    period, direction, fpt, amp, phase, re, im = mats  # unpack
    # package for returning
    tfs = Record("wave_elevation")
    tfs.addattr(amp=amp, phase=phase, re=re, im=im,
                dirs=direction, pers=period,
                directions=directions, periods=periods)
    return tfs
