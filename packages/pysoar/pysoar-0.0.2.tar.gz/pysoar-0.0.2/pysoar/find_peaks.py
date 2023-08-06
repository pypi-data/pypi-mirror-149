import numpy as np
import matplotlib.pyplot as plt

def findTime(indx, s2, time):
    ix = []
    ix_loc = np.where(s2[indx] == max(s2[indx]))[0][0]
    ix.append(ix_loc)
    ix.append(time[indx[ix_loc]])

    return ix


def find_peaks(Count, PoisLamda, thresh, time):
    """
    Args:
        Count: Clean current
        PoisLamda: Baseline current value
        thresh: Threshold value
        time: Time data points

    Returns:
        Arrays containing the following informattion: time at which the the peak occured, maximum current value
        of the peak, mean current value of the peak, start of the event, end of the event, peak's index.
    """

    s = np.copy(Count)
    CountBase = np.copy(Count)
    time_plot = np.copy(time)
    noise = np.random.rand(1, len(s)) * 1e-9
    noise = noise[0]
    Data = np.copy(s + noise)

    s[s < PoisLamda] = 0

    p = abs(np.sign(s))

    ps = np.diff(p)
    ps = np.insert(ps, 0, p[0])

    ps[ps != 1] = 0
    ps = np.cumsum(ps)
    ps = ps * p

    s = s[p != 0]
    p = ps[ps != 0]

    m = []
    for i in np.unique(p):
        m.append(max(s[p == i]))

    FndAboveThresh = np.where(m >= thresh)[0]
    FndAboveThresh = FndAboveThresh + 1
    ind_new = np.isin(ps,
                      FndAboveThresh)

    s2 = Data[ind_new]
    time = time[ind_new]

    ind_new_int = ind_new * 1

    ind_new2 = np.diff(ind_new_int)
    ind_new2 = np.insert(ind_new2, 0, ind_new_int[0])
    ind_new2[ind_new2 != 1] = 0

    ind_new2 = np.cumsum(ind_new2)
    ind_new2 = ind_new2 * ind_new
    ind_new3 = ind_new2[ind_new2 != 0]

    first = []
    last = []
    MeanBurst = []
    SUM = []

    for i in np.unique(ind_new3):
        first.append(s2[ind_new3 == i][0])
        last.append(s2[ind_new3 == i][-1])
        MeanBurst.append(np.mean(s2[ind_new3 == i]))
        SUM.append(sum(s2[ind_new3 == i]))

    Output = []
    numel_s2 = np.arange(0, len(s2))
    for i in np.unique(ind_new3):
        Output.append(findTime(numel_s2[ind_new3 == i], s2, time))

    Output = np.array(Output)

    SUM = np.array(SUM)
    first = np.array(first)
    last = np.array(last)
    MeanBurst = np.array(MeanBurst)

    TiMaxBurst = Output[:, 1]

    PkMaxBurst = []
    FndAboveThresh = FndAboveThresh - 1
    for i in FndAboveThresh:
        PkMaxBurst.append(m[i])

    PkMaxBurst = np.array(PkMaxBurst)

    TiLow = []
    TiHigh = []
    for i in np.unique(ind_new3):
        TiLow.append(time[ind_new3 == i][0])
        TiHigh.append(time[ind_new3 == i][-1])

    TiLow = np.array(TiLow)
    TiHigh = np.array(TiHigh)

    PeakIndex = Output[:, 1]

    plt.figure(figsize=[30, 10])
    plt.plot(TiMaxBurst, PkMaxBurst, marker='o', linestyle='', mfc='none', c='r', label='Maximum Value')
    plt.plot(TiMaxBurst, MeanBurst, marker='x', linestyle='', c='r', label='Mean Value')
    plt.plot(time_plot, CountBase, alpha=0.5)
    plt.axhline(PoisLamda, c='lime', label='Baseline')
    plt.axhline(thresh, c='k', label='Threshold')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (nA)')
    plt.legend(loc='upper right')
    plt.show()

    return TiMaxBurst, PkMaxBurst, MeanBurst, TiLow, TiHigh,PeakIndex


