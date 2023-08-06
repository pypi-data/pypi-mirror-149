import pandas as pd
from scipy.integrate import cumtrapz
import numpy as np
import matplotlib.pyplot as plt

def calculate_capacitance(current, frequency, V_out, W, L, n_tft=500):
    """
    Function that calculates capacitance from I-V data recorded. Since data are
    acquired as AC signal then C = I/(2*pi*f*V_out)

    Parameters
    ----------
    current : float
        Current value registered from lock-in amplifier
    frequency : float
        DFrequency of acquisition
    V_out : float
        RMS of peak-to-peak value of base voltage in lock-in amplifier
    W : float
        Width of the transistor's channel in meters
    L : float
        Length of the transistor's channel in meters
    n_tft : int, optional
        Numer of trasistors in the sample. The default is 500.

    Returns
    -------
    C : float
        Values of capacitance

    """
    C = current /(2*3.1415*frequency*V_out)
    C = C-min(C) #remove parasite capacitance
    return C

def calculate_DOS(capacitance, oxide_capacitance, W, L, t):
    q0 = 1.6e-19
    CD = (capacitance*oxide_capacitance) / (oxide_capacitance-capacitance)
    g= CD /(q0*W*L*t)
    return g

def calculate_energy_range(capacitance, oxide_capacitance, voltage, correction=0, init = 0):
    E = cumtrapz(1-capacitance/oxide_capacitance,voltage, initial = init)+correction
    return E

def find_fit_interval(E, g, FitLeft, FitRight):
    fit_interval = np.where((E>=FitLeft) & (E<=FitRight))
    fit_interval = fit_interval[0]
    g = g[fit_interval]
    E = E[fit_interval]
    return E, g

