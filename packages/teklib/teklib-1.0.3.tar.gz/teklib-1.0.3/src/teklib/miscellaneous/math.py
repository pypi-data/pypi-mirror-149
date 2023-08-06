import numpy as np
from abc import ABC, abstractmethod

def interpc(x, xp, fp):
  """ Alternative to numpy interp for complex numbers where the abs and phase are interpolated"""
  return np.interp(x, xp, np.abs(fp))*np.exp(1j*np.interp(x, xp, np.abs(fp)))

def complex_interp2d(xi, yi, x, y, z, use_phase=False):
    """ Interpolates a 2d complex array z(x,y) to z(xi,yi)
    interp2d originates from the image processing community:

    Image processing community, f(x,y)   .... x is across the screen i.e. columns!
    Algebra community,          f[ix,iy] .... ix is a row index .... so ....

    zi = I(xi,yi); I  = interp2d(x,y,z) generates a matrix zi of shape (len(yi), len(xi))
    """
    from scipy.interpolate import RectBivariateSpline
    func1 = RectBivariateSpline(x, y, np.abs(z) if use_phase else z.real)
    func2 = RectBivariateSpline(x, y, np.angle(z) if use_phase else z.imag)
    if use_phase:
        return np.ravel(np.r_[[func1(i,j) * np.exp(1j*func2(i,j)) for i, j in zip(xi, yi)]])
    else:                 
        return np.ravel(np.r_[[func1(i,j) + 1j*func2(i,j) for i, j in zip(xi, yi)]])


# Rotation Matrix Class
class RotatorInterface(ABC):
    @abstractmethod
    def rmat(): 
        """ Returns the rotation matrix """
        raise NotImplementedError("Should have implemented this")

class AxisAngleRotator(RotatorInterface):
    def __init__(self, axis:np.ndarray=np.r_[1,0,0], angle:float=0):
        self.axis = axis/np.linalg.norm(axis)
        self.angle = angle
        
    def rmat(self, trans:bool=False)->np.ndarray:
        """ 
        If trans is False (default):
            returns a rotation matrix for rotating a vector in a coordinate system to a new position
            Can be used to rotate the body's global coordinates to a new position in the global c-sys. 
            Inputs are heel angle and axis of rotation. Right hand rule applies
        Otherwise:
            returns a transformation matrix for transforming a global vector to the body-fixed system
            Can be used to express the global forces in terms of the new body-fixed position.
            This is in essence the inverse operation however semantically there are differences. 
        """
        ux, uy, uz = self.axis
        a = self.angle
        c, s = np.cos(a*np.pi/180), np.sin(a*np.pi/180)
        A =  np.array([
                  [c + ux**2*(1-c), ux*uy*(1-c)-uz*s, ux*uz*(1-c)+uy*s],
                  [ux*uy*(1-c)+uz*s, c + uy**2*(1-c), uy*uz*(1-c)-ux*s],
                  [ux*uz*(1-c)-uy*s, uy*uz*(1-c)+ux*s, c + uz**2*(1-c)]
                  ])
        return A.T if trans else A

class AxisAngleYawRotator(RotatorInterface):
    def __init__(self, axis:np.ndarray=np.r_[1,0,0], angle:float=0, yaw:float=0):
        self.axis = axis/np.linalg.norm(axis)
        self.angle = angle
        self.yaw = yaw
       
    def rmat(self, trans:bool=False)->np.ndarray:
        """ 
        If trans is False (default):
            returns a rotation matrix for rotating a vector in a coordinate system to a new position
            Can be used to rotate the body's global coordinates to a new position in the global c-sys. 
            Inputs are heel angle and axis of rotation and body yaw. Right hand rule applies. First the
            body is heeled and then it is yawed about the global z-axis.
        Otherwise:
            returns a transformation matrix for transforming a global vector to the body-fixed system
            Can be used to express the global forces in terms of the new body-fixed position.
            This is in essence the inverse operation however semantically there are differences. 
        """
        ux, uy, uz = self.axis
        a = self.angle
        c, s = np.cos(a*np.pi/180), np.sin(a*np.pi/180)
        A =  np.array([
                  [c + ux**2*(1-c), ux*uy*(1-c)-uz*s, ux*uz*(1-c)+uy*s],
                  [ux*uy*(1-c)+uz*s, c + uy**2*(1-c), uy*uz*(1-c)-ux*s],
                  [ux*uz*(1-c)-uy*s, uy*uz*(1-c)+ux*s, c + uz**2*(1-c)]
                  ])
        c, s = np.cos(self.yaw*np.pi/180), np.sin(self.yaw*np.pi/180)
        rz = np.array([[c,-s,0],[s,c,0],[0,0,1]])
        A = rz@A
        return A.T if trans else A

class EulerRotator(RotatorInterface):
    def __init__(self, roll=0, pitch=0, yaw=0, convention="z-y-x"):
        self.angles = np.r_[roll, pitch, yaw]
        self.convention=convention

    def rmat(self, trans:bool=False)->np.ndarray:
        """ 
        If trans is False (default):
            returns a rotation matrix for rotating a vector in a coordinate system to a new position
            using Euler angles following a certain convention. Right hand rule applies.
            convention="z-y-x" means the body is first rotated by angles[2] about the z-axis
            then by angles[1] about the new y-axis and finally by angles[0] about the new x-axis.
            This is an intrinsic operation which means that the rotations are performed opposite
            to how they have been verbalized. 
        Otherwise:
            returns a transformation matrix for transforming a global vector to the body-fixed system
            Can be used to express the global forces in terms of the new body-fixed position.
            This is in essence the inverse operation however semantically there are differences. 
        """
        a1, a2, a3 = self.angles*np.pi/180.
        c, s = np.cos, np.sin
        rx = np.array([[1,0,0],[0,c(a1),-s(a1)],[0,s(a1),c(a1)]])
        ry = np.array([[c(a2),0,s(a2)],[0,1,0],[-s(a2),0,c(a2)]])
        rz = np.array([[c(a3),-s(a3),0],[s(a3),c(a3),0],[0,0,1]])
        r = {"x":rx, "y": ry, "z":rz}
        A = np.eye(3)
        for axis in self.convention.split('-')[::-1]: A = r[axis]@A
        return A.T if trans else A

class QuaternionRotator(RotatorInterface): pass