import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.special import gamma



def threshold(CountBase, Time, STD, SO, Overide, OverideStep, OverideMax):
    """
    Args:
        CountBase: Clean current
        Time: Time data points
        STD: Cutoff value in terms of standard deviation
        SO: Step offset
        Overide: Boolean value, if the user wants to input parameters manually (1) or not (0)
        OverideStep: Width of the bins
        OverideMax: Maximum current value taken into the account
    Returns:
        Threshold value, baseline value, bin ranges, number of values within each bin and the Poisson fit
    """
    Df = np.diff(CountBase)
    Step = np.mean(abs(Df))

    if Step < 0.001:
        Step = 0.001

    StepVec = np.arange(0, max(CountBase) / 2+Step, Step)

    Mx = max(CountBase)/2

    if len(StepVec) < 25:
        Step = Step / 2
        StepVec = np.arange(0, max(CountBase) / 2+Step, Step)

    if Overide:
        Step = OverideStep
        StepVec = np.arange(0, OverideMax+Step, Step)
        Mx = OverideMax

    Hist, edges = np.histogram(CountBase,
                                 StepVec)

    StepVec=StepVec[:-1]


    Hist = Hist / sum(Hist)
    Hist = Hist[1:]
    StepVec = StepVec[1:]

    Pois = lambda x, u: u ** x * np.exp(-u) / gamma(x + 1)

    PoisLamda = curve_fit(Pois, np.arange(1, len(StepVec) + 1), Hist)
    PoisLamda = PoisLamda[0][0]

    PoisFit = Pois(np.arange(1, len(StepVec)+1), PoisLamda)
    PoisFit = PoisFit / max(PoisFit) * max(Hist)

    thresh = PoisLamda + STD * math.sqrt(PoisLamda)
    thresh = thresh * Step
    PoisLamda = PoisLamda * Step * SO

    plt.figure(figsize=[12, 8])
    plt.semilogy(StepVec, Hist, marker='x', linestyle='')
    plt.semilogy(StepVec, PoisFit, 'r')
    plt.axvline(thresh, color='k')
    plt.text(thresh+0.001, 0.01, 'Threshold = ' + str(thresh) + ' nA')
    plt.ylabel('Frequency')
    plt.xlabel('Current (nA)')
    plt.xlim(0, Mx)
    plt.ylim(1e0, 1e-5)
    plt.show()

    plt.figure(figsize=[12, 8])
    plt.plot(Time, CountBase)
    plt.axhline(thresh, color='k', label='Threshold')
    plt.axhline(PoisLamda, color='lime', label='Baseline')
    plt.ylabel('Current (nA)')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.show()

    return thresh, PoisLamda, StepVec, Hist, PoisFit



