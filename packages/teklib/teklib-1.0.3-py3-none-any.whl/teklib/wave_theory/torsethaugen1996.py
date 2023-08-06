#-------------------------------------------------------------------------#
#   TORSETHAUGEN (1996) WAVE SPECTRUM
#-------------------------------------------------------------------------#
#   modelled according to dnv c205 2010 p 110*
#   * wave spectrum is modified by a factor h1 and h2 to ensure that output
#   Hm0 is equal to the Hs
#
#   [S] = torsethaugen(Hs,Tp,ps,t_limit)
#
#   Hs:         significant wave height [m]
#   Tp:         spectral peak period [sec]
#   ps:         plot spectrum in figure
#   wave_spectrum:  matlab struct containing spectrum parameters
#   t_limit:    variable that can be left default the spectrum will then
#               be defined from 3 to 40 sec. [t_low t_high] can also be defined
#               as the boundary values for spectrum generation
#
#   af:         fetch length. set to 6.6
#
#   example:    torsethaugen(16.3,16.9,1)
#   example:    torsethaugen(16.3,16.9,0,[5 25])
#
#   10.09.2019: Converted to python to compare with SIMO
#
#-------------------------------------------------------------------------#


def torsethaugen1996(Hs, Tp, w=None, ps=False, t_limit=None):

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.special import gamma
    import sys

    # response variables
    wave_spectrum = {}
    g = 9.81

    # number of frequency components

    if t_limit is None:
        f_low = 1/40
        f_high = 1/3
    else:
        f_low = 1/t_limit[1]
        f_high = 1/t_limit[0]

    # fetch length
    af = 6.6

    # wind or swell distinction
    Tf = af * Hs ** (1/3.)
    if Tp <= Tf:
        sd = 'wind'
    elif Tp > Tf:
        sd = 'swell'

    # for all frequencies
    if w is not None:
        frequencies = w/2/np.pi + 0.0001
        ncomp = len(frequencies)
    else:
        ncomp = 200
        df = (f_high - f_low)/ncomp
        frequencies = np.arange(f_low, f_high, df)

    S = np.zeros((len(frequencies), 4))

    for fc, f in enumerate(frequencies):

        # common parameters
        N = 0.5 * np.sqrt(Hs) + 3.2

        #---------------------------------------------------------------------#
        # if wind dominated seas
        #---------------------------------------------------------------------#
        if sd == 'wind':

            rpw = 0.7 + 0.3 * np.exp(-(2*(Tf - Tp)/(Tf - 2*sqrt(Hs)))**2)

            # primary peak
            HS1 = rpw * Hs
            TP1 = Tp
            M = 4
            gma1 = 35. * (1 + 3.5*np.exp(-Hs)) * (2*np.pi/g * HS1/Tp**2)**0.857
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma1 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma1)**f2 + 1.0) / gma1
            fn1 = f * TP1
            if fn1 < 1:
                sig = 0.07
            elif fn1 >= 1:
                sig = 0.09

            gmaF1 = gma1 ** np.exp(-1/(2*sig**2)*(fn1 - 1)**2)
            GMAS1 = fn1 ** -N * np.exp(-N/M * fn1**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn1 = G0 * Agma1 * GMAS1 * gmaF1
            E1 = 1/16. * HS1**2 * TP1

            # secondary peak
            HS2 = np.sqrt(1-rpw**2)*Hs
            TP2 = Tf + 2.0
            M = 4
            gma2 = 1.
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma2 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma2)**f2 + 1) / gma2
            gmaF2 = 1.
            fn2 = f * TP2
            GMAS2 = fn2 ** -N * np.exp(-N/M * fn2**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn2 = G0 * Agma2 * GMAS2 * gmaF2
            E2 = 1/16. * HS2**2 * TP2

            #---------------------------------------------------------------------#
            # if swell dominated seas
            #---------------------------------------------------------------------#
        elif sd == 'swell':

            rps = 0.6 + 0.4 * np.exp(-((Tp - Tf)/(0.3 * (25 - Tf)))**2)

            # primary peak
            # disp('primary peak')
            HS1 = rps * Hs
            TP1 = Tp
            gma1 = 35. * (1 + 3.5*np.exp(-Hs)) * (2*np.pi/g * Hs/Tf **
                                                  2)**0.857 * (1. + 6*((Tp - Tf) / (25. - Tf)))
            M = 4.
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma1 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma1)**f2 + 1.) / gma1
            fn1 = f * TP1
            if fn1 < 1:
                sig = 0.07
            elif fn1 >= 1:
                sig = 0.09

            gmaF1 = gma1 ** np.exp(-1/(2*sig**2)*(fn1 - 1)**2)
            GMAS1 = fn1 ** -N * np.exp(-N/M * fn1**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn1 = G0 * Agma1 * GMAS1 * gmaF1
            E1 = 1/16. * HS1**2 * TP1

            # secondary peak
            # disp('secondary peak')
            HS2 = np.sqrt(1-rps**2)*Hs
            G0 = (1/M * (N/M) ** (-(N-1.)/M) * gamma((N-1.)/M)) ** -1
            s4 = np.max([0.01, 0.08 * (1. - np.exp(-1/3 * Hs))])
            tmp = ((16. * s4 * 0.4 ** N) / (G0 * HS2**2)) ** (-1./(N-1.))
            TP2 = np.max([2.5, tmp])
            gma2 = 1
            M = 4. * (1 - 0.7 * np.exp(-1/3 * Hs))
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma2 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma2)**f2 + 1) / gma2
            gmaF2 = 1.
            fn2 = f * TP2
            GMAS2 = fn2 ** -N * np.exp(-N/M * fn2**-M)
            Sn2 = G0 * Agma2 * GMAS2 * gmaF2
            E2 = 1./16. * HS2**2 * TP2

        # spectrum frequency
        S[fc, 0] = f

        # primary spectrum
        S[fc, 1] = E1 * Sn1

        # secondary spectrum
        S[fc, 2] = E2 * Sn2

    # including factor to correct primary and secondary spectrum to input Hs
    f = S[:, 0]
    a1 = np.trapz(f**0 * S[:, 1], f)
    a2 = np.trapz(f**0 * S[:, 2], f)

    h1 = HS1**2 / (4*np.sqrt(a1))**2
    h2 = HS2**2 / (4*np.sqrt(a2))**2

    # corrected primary and secondary peak (to ensure Hm0 = Hs)
    S[:, 1] = S[:, 1] * h1
    S[:, 2] = S[:, 2] * h2
    S[:, 3] = S[:, 1] + S[:, 2]

    # calculating spectrum moments
    Sf = S[:, 3]
    m0 = np.trapz(f**0 * Sf, f)
    m1 = np.trapz(f**1 * Sf, f)
    m2 = np.trapz(f**2 * Sf, f)

    # calculating statistical parameters
    Hm0 = 4 * np.sqrt(m0)
    Tm01 = m0 / m1
    Tm02 = np.sqrt(m0/m2)

    wave_spectrum['spectrum'] = S
    wave_spectrum['m0'] = m0
    wave_spectrum['m1'] = m1
    wave_spectrum['m2'] = m2
    wave_spectrum['Hm0'] = Hm0
    wave_spectrum['Tm01'] = Tm01
    wave_spectrum['Tm02'] = Tm02

    # plot
    if ps is True:

        fig = plt.figure(figsize=(8, 12))
        ax1 = fig.add_subplot(4, 1, 1)
        ax1.plot(f, Sf)
        ax1.set_title('Torsethaugen 1996 wave spectrum Hs ' +
                      str(Hs) + ' m Tp ' + str(Tp) + ' s')
        ax1.set_xlabel('Hz [1/sec]')
        ax1.set_ylabel('S(f) m**2s')
        ax1.set_xlim(f_low, f_high)
        ax1.grid(True)

        ax2 = fig.add_subplot(4, 1, 2)
        ax2.plot(f*(2*np.pi), Sf/(2*np.pi))
        ax2.set_xlabel('w [rad/sec]')
        ax2.set_ylabel('S(w) m**2s/rad')
        ax2.set_xlim(2*np.pi*f_low, 2*np.pi*f_high)
        ax2.grid(True)

        ax3 = fig.add_subplot(4, 1, 3)
        ax3.plot(1./f, Sf)
        ax3.set_xlabel('T [sec]')
        ax3.set_ylabel('S(f) m**2s')
        ax3.set_xlim(1/f_high, 1/f_low)
        ax3.grid(True)

        ax4 = fig.add_subplot(4, 1, 4)
        ax4.plot(1./f, S[:, 1], label='primary peak')
        ax4.plot(1./f, S[:, 2], label='secondary peak')
        ax4.set_xlabel('T [sec]')
        ax4.set_ylabel('S(f) m**2s')
        ax4.legend(loc=0)
        ax4.set_xlim(1/f_high, 1/f_low)
        ax4.grid(True)
        plt.show()

    if w is None:
        return Sf/(2*np.pi), f*2*np.pi
    else:
        return Sf/(2*np.pi)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    w = np.linspace(0, 5, 254)
    #Sf, w = torsethaugen1996(4, 16)
    Sf = torsethaugen1996(4, 16, w)
    plt.plot(w, Sf)
    plt.show()
