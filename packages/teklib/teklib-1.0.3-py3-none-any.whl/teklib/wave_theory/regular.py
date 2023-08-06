import numpy as np
from abc import ABC, abstractmethod, abstractproperty

def wave_params(Ap=5, Tp=10, h=1000):
    """
        DNV C205 parameters for assessing regular waves
    """
    g = 9.80665 # m/s/s
    Lp = Tp**2*g/2/np.pi
    H = 2*Ap
    h =  min(h, 0.8*Lp) # m TODO: (remove - temporary hack for CFD comparisons)
    w = 2*np.pi/Tp
    k = w**2/g # be lazy (apply deep water relation)                                              
    s = np.tanh(k*h)
    stokes_2nd = 1 + k*Ap*(3-s**2)/4/s**3
    wave_steepness_param = S = H/Lp
    shallow_water_param = mu = h/Lp
    ursells_nr = ur = S/mu**3 # H*Lp**2/h**3
    return stokes_2nd, S, mu, ur

class RegularWave(ABC):
    """ Abstract class for regular waves """
    @abstractproperty
    def height(self): pass
    @abstractproperty
    def period(self): pass
    @abstractproperty
    def phase(self): pass
    @abstractproperty
    def wavelength(self): pass
    @abstractproperty
    def wavenumber(self): pass
    @abstractproperty
    def crest_level(self): pass
    @abstractproperty
    def trough_level(self): pass
    @abstractproperty
    def group_velocity(self): pass
    @abstractproperty
    def phase_velocity(self): pass


class StokesFirst(RegularWave):
    """
        First-order Stokes wave implementation
    """
    def __init__(self, height, period, phase=0, depth=1000, g=9.80665):
        self.__gravity = g
        self.__depth = depth
        self.__height = height
        self.__period = period
        self.__phase = phase
        self.__wavenumber = self.__compute_wavenumber()
        k, d = self.__wavenumber, depth
        self.__wavelength = 2*np.pi/k
        self.__crest_level = height/2
        self.__trough_level = height/2
        self.__phase_velocity = (g/k*np.tanh(k*d))**0.5
        self.__group_velocity = self.phase_velocity*(1+2*k*d/np.sinh(2*k*d))

    @property
    def height(self): return self.__height
    @property
    def period(self): return self.__period
    @property
    def phase(self): return self.__phase
    @property
    def wavelength(self): return self.__wavelength
    @property
    def wavenumber(self): return self.__wavenumber
    @property
    def crest_level(self): return self.__crest_level
    @property
    def trough_level(self): return self.__trough_level
    @property
    def group_velocity(self): return self.__group_velocity
    @property
    def phase_velocity(self): return self.__phase_velocity

    def surface_elevation(self, x, t):
        theta = self.__wavenumber*(x-self.__phase_velocity*t) + self.phase
        return self.__height/2*np.cos(theta)

    def horizontal_velocity():
        pass

    #@classmethod
    def __compute_wavenumber(self, g = 9.80665):
        """ Returns the wave number satisfying the first order linear dispersion relation 
            w**2 = gktanh(kh)
        """
        from scipy.optimize import root_scalar
        # To relax requirement on input allow for both iterable and non-iterable inputs
        wi = 2*np.pi / self.__period
        h = self.__depth
        sol = root_scalar(lambda k_, h, w: w**2 - g*k_*np.tanh(k_*h), 
                                args=(h, wi), method='brentq', bracket=[0, 10])
        if not sol.converged: print(f"Period {2*np.pi/wi} is not converged.")
        return sol.root


class StokesSecond(RegularWave):
    """
        Second-order Stokes wave implementation
    """
    def __init__(self, height, period, phase=0, depth=1000, g=9.80665):
        self.__gravity = g
        self.__depth = depth
        self.__height = height
        self.__period = period
        self.__phase = phase
        self.__wavenumber = self.__compute_wavenumber()
        k, d, a = self.__wavenumber, depth, height/2
        s = np.tanh(k*d)
        self.__wavelength = 2*np.pi/k
        self.__crest_level = a * (1 + k*a*(3-s**2)/(4*s**3))
        self.__trough_level = -a * (1 - k*a*(3-s**2)/(4*s**3))
        self.__phase_velocity = (g/k*np.tanh(k*d))**0.5
        self.__group_velocity = self.phase_velocity*(1+2*k*d/np.sinh(2*k*d))

    @property
    def height(self): return self.__height
    @property
    def period(self): return self.__period
    @property
    def phase(self): return self.__phase
    @property
    def wavelength(self): return self.__wavelength
    @property
    def wavenumber(self): return self.__wavenumber
    @property
    def crest_level(self): return self.__crest_level
    @property
    def trough_level(self): return self.__trough_level
    @property
    def group_velocity(self): return self.__group_velocity
    @property
    def phase_velocity(self): return self.__phase_velocity

    def surface_elevation(self, x, t):
        theta = self.__wavenumber*(x-self.__phase_velocity*t) + self.phase
        kd, H, L = self.__wavenumber*self.__depth, self.__height, self.__wavelength
        linear = H/2*np.cos(theta)
        second = np.pi*H**2/8/L*np.cosh(kd)/np.sinh(kd)**3*(2+np.cosh(2*kd))*np.cos(2*theta)
        return linear + second

    #@classmethod
    def __compute_wavenumber(self):
        """ Returns the wave number satisfying the first order linear dispersion relation 
            w**2 = gktanh(kh)
        """
        from scipy.optimize import root_scalar
        # To relax requirement on input allow for both iterable and non-iterable inputs
        wi = 2*np.pi / self.__period
        h = self.__depth
        g = self.__gravity
        sol = root_scalar(lambda k_, h, w: w**2 - g*k_*np.tanh(k_*h), 
                                args=(h, wi), method='brentq', bracket=[0, 10])
        if not sol.converged: print(f"Period {2*np.pi/wi} is not converged.")
        return sol.root



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    first_order = StokesFirst(height=5, period=10, depth=300)
    second_order = StokesSecond(height=5, period=10, depth=300)
    print(first_order.wavelength)
    print(first_order.wavenumber, 2*np.pi/(first_order.wavenumber*9.80665)**.5, first_order.wavelength/first_order.phase_velocity)
    print(first_order.phase_velocity)
    print(first_order.phase_velocity*first_order.period)

    print(first_order.crest_level)
    print(second_order.crest_level, second_order.trough_level)
    print(second_order.crest_level - second_order.trough_level)

    x = np.linspace(0, 2*second_order.wavelength, 1000)
    plt.plot(x, second_order.surface_elevation(x,t=0), label="second")
    plt.plot(x, first_order.surface_elevation(x,t=0), label="first")
    plt.axhline(second_order.crest_level)
    plt.legend(loc=0)
    plt.show()
