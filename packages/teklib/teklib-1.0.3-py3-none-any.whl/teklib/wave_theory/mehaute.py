import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import importlib.resources as pkg_resources


def mehaute(wave_params=None):
    """
    Wave theory categorization plot
    wave_params(H, h, T)
    H - wave height
    h - water depth
    T - wave period
    """

    # Setup plot
    fig, ax = plt.subplots(1,1,figsize=(8,6))
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Read the data
    fname = os.path.join(os.path.dirname(__file__), "mehaute.txt")
    x, y = np.loadtxt(fname, delimiter=",").T # data points

    # Shallow water and deep water boundary lines
    shallow_water, deep_water = x[2:4]

    # Linear wave theory
    linear_x = np.r_[x[0],x[6:28]]
    linear_y = np.r_[y[0],y[6:28]]
    # Stokes 2nd order
    second_x = np.r_[x[28:42]]
    second_y = np.r_[y[28:42]]
    # Stokes 3rd order
    third_x = np.r_[x[4],x[42:53]]
    third_y = np.r_[y[4],y[42:53]]
    # Stokes 4th/5th order
    fourth_x = np.r_[x[5],x[53:60]]
    fourth_y = np.r_[y[5],y[53:60]]
    # breaking criteria
    break_x = np.r_[x[0],x[1]]
    break_y = np.r_[y[0],y[1]]    
    # plot 
    ax.set_xlim(0.0001, 1.0)
    ax.set_ylim(0.00001, 0.1)
    ax.plot(linear_x, linear_y)
    ax.plot(second_x, second_y)
    ax.plot(third_x, third_y)
    ax.plot(fourth_x, fourth_y)
    ax.plot(break_x, break_y)
    ax.axvline(shallow_water, linestyle='--')
    ax.axvline(deep_water, linestyle='--')
    ax.text(0.00015, 0.11, "Shallow water")
    ax.text(0.003, 0.11, "Intermediate depth")
    ax.text(0.13, 0.11, "Deep water")
    ax.text(0.13, 0.0001, "Linear")
    ax.text(0.13, 0.003, "Stokes 2nd")
    ax.text(0.13, 0.013, "Stokes 3rd")
    ax.text(0.0002, 0.00005, "Cnoidal")
    ax.text(0.00048, 0.000335, "Solitary", rotation = 35)
    ax.set_xlabel("$\dfrac{h}{gT^2}$")
    ax.set_ylabel("$\dfrac{H}{gT^2}$", rotation = 0)

    if wave_params is not None:
        H, T, h = wave_params
        g = 9.80665
        x = h/g/T**2
        y = H/g/T**2
        print(x, y)
        ax.scatter(x, y, label="Conditions")

    plt.show()



if __name__ == "__main__":
    H = 4 #np.r_[4, 16] 
    T = 10 #np.r_[10, 20]
    h = 1000
    mehaute(wave_params=(H, T, h))