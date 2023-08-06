import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

class Translocations:
    def __init__(self):
        self.Fit = {}
        self.CountsExtract = {}
        self.TimeExtract = {}
        self.TimeEvent = {}
        self.MEAN = {}
        self.icp = {}
        self.NumberOfLevels = {}
        self.NoSubPeaks = {}
        self.std = {}
        self.ADEPT_params = {}
        self.ADEPT_curr_max = {}
        self.DwellTime = {}
        self.PeakHeight = {}

    def cusum(self, num, TiLow, TiHigh):
        """
        Args:
            num: index of the event
            TiLow: array containing the start time of the events
            TiHigh: array containing the end of the events

        Returns:
             A plot of the event with the CUSUM fit in red

        """

        plt.plot(self.TimeExtract[num], self.CountsExtract[num])
        plt.ylabel('Current (nA)')
        plt.xlabel('Time (s)')

        for i in range(len(self.icp[num])):
            brk = self.icp[num][i]

            if i == 0:
                plt.plot(self.TimeExtract[num][:brk + 1], self.Fit[num][i].repeat(len(self.TimeExtract[num][:brk + 1])),
                         c='r')
                plt.plot(self.TimeExtract[num][brk].repeat(2), [self.Fit[num][i], self.Fit[num][i + 1]], c='r')
                plt.plot(self.TimeExtract[num][brk:self.icp[num][i + 1]],
                         self.Fit[num][i + 1].repeat(len(self.TimeExtract[num][brk:self.icp[num][i + 1]])), c='r')

            elif i == len(self.icp[num]) - 1:
                plt.plot(self.TimeExtract[num][brk].repeat(2), [self.Fit[num][i], self.Fit[num][i + 1]], c='r')
                plt.plot(self.TimeExtract[num][brk:], self.Fit[num][i + 1].repeat(len(self.TimeExtract[num][brk:])),
                         c='r')

            else:
                plt.plot(self.TimeExtract[num][brk].repeat(2), [self.Fit[num][i], self.Fit[num][i + 1]], c='r')
                plt.plot(self.TimeExtract[num][brk:self.icp[num][i + 1]],
                         self.Fit[num][i + 1].repeat(len(self.TimeExtract[num][brk:self.icp[num][i + 1]])), c='r')

        plt.axvline(TiLow[num], c='black', linestyle='--')
        plt.axvline(TiHigh[num], c='black', linestyle='--')
        plt.show()

        print('Number of levels ' + str(self.NumberOfLevels[num]))
        print('Number of sub peaks ' + str(self.NoSubPeaks[num]))
        print('Translocation Time = ' + str(self.DwellTime[num]) + ' ms')
        print('Peak Amplitude = ' + str(self.PeakHeight[num]) + ' nA')


    def adept(self, num, TiLow, TiHigh):
        """
        Args:
            num: index of the event
            TiLow: array containing the start time of the events
            TiHigh: array containing the end of the events

        Returns:
             A plot of the event with the ADEPT fit in purple
        """

        dt = 1e-9

        x = self.CountsExtract[num]
        t = self.TimeExtract[num]
        TiLow_c = TiLow[num]
        TiHigh_c = TiHigh[num]

        deltaT = np.diff(t)
        deltaT = deltaT[0]

        BinLow = round((TiLow_c - min(t)) / deltaT + dt) - 8

        i0_left = np.mean(x[:BinLow + 1])
        b = i0_left

        a = max(x) - i0_left
        tau = deltaT
        mu1 = TiLow_c
        mu2 = TiHigh_c

        if len(self.MEAN[num][:, 11]) > 2:
            mu2 = self.MEAN[num][-1, 11]

        NoSubPeaks = self.NoSubPeaks[num]

        if NoSubPeaks > 1:
            NoSubPeaks = 1

        N = NoSubPeaks + 2

        if N == 2:
            d1 = np.repeat(a, N)
            starting = np.append(d1, [b, mu1, mu2])
            d2 = np.repeat(deltaT, N)
            starting = np.append(starting, d2)

            d3 = np.repeat(-5, N)
            lb = np.append(d3, [-20, TiLow_c - 1, TiHigh_c - 0.1])
            d4 = np.repeat(deltaT, N)
            lb = np.append(lb, d4)

            d5 = np.repeat(5, N)
            ub = np.append(d5, [20, TiLow_c + 1, TiHigh_c + 0.1])
            d6 = np.repeat(deltaT * 1e2, N)
            ub = np.append(ub, d6)

            FD, pcov = curve_fit(FitFuncTwo, t, x, bounds=(lb, ub), p0=starting)
            self.ADEPT_params[num] = FD
            StepRes = FitFuncTwo(t, FD[0], FD[1], FD[2], FD[3], FD[4], FD[5], FD[6])
            self.ADEPT_curr_max[num] = max(FitFuncTwo(t, FD[0], FD[1], FD[2], FD[3], FD[4], FD[5]*5, FD[6]*5))

        elif N == 3:
            a = max(abs(self.MEAN[num][2:-1, 6]))
            LOC = np.where(abs(self.MEAN[num][2:-1, 6])==a)[0][0]
            Sn = np.sign(self.MEAN[num][2+LOC, 6])
            LOC = np.where(self.MEAN[num][:,6]<0)[0]

            if Sn > 0:
                mu12 = self.MEAN[num][LOC[0]-1,11]
            else:
                mu12 = self.MEAN[num][LOC[0],11]

            a1 = self.MEAN[num][LOC[0]-1, 10]
            a2 = max(abs(self.MEAN[num][2:-1, 6]))*Sn
            a3 = self.MEAN[num][-1,6]

            starting = np.array([a1, a2, a3, b, mu1, mu12, mu2])
            starting = np.append(starting, np.repeat(deltaT, N))

            d1 = np.repeat(-5, N)
            lb = np.append(d1, [-20, TiLow_c - 0.5, self.MEAN[num][1, 11], self.MEAN[num][-2, 12]])
            lb = np.append(lb, np.repeat(deltaT, N))

            d2 = np.repeat(5, N)
            ub = np.append(d2, [20, TiLow_c + 0.5, self.MEAN[num][-2, 12], TiHigh_c + 0.1])
            ub = np.append(ub, np.repeat(deltaT * 1e3, N))

            FD, pcov = curve_fit(FitFuncThree, t, x,bounds=(lb, ub), p0 = starting)
            self.ADEPT_params[num] = FD
            StepRes = FitFuncThree(t, FD[0], FD[1], FD[2], FD[3], FD[4], FD[5], FD[6], FD[7], FD[8], FD[9])
            self.ADEPT_curr_max[num] = max(FitFuncThree(t, FD[0], FD[1], FD[2], FD[3], FD[4], FD[5], FD[6], FD[7]*5,
                                                        FD[8]*5, FD[9]*5))

        plt.plot(t, x)
        plt.plot(t, StepRes, c='purple')
        plt.axvline(TiLow[num], c='black', linestyle='--')
        plt.axvline(TiHigh[num], c='black', linestyle='--')
        plt.ylabel('Current (nA)')
        plt.xlabel('Time (s)')
        plt.show()
        print('Number of levels ' + str(self.NumberOfLevels[num]))
        print('Number of sub peaks ' + str(self.NoSubPeaks[num]))
        print('Translocation Time = ' + str(self.DwellTime[num]) + ' ms')
        print('Peak Amplitude = ' + str(self.PeakHeight[num]) + ' nA')

    def hist_time(self, width, low, up):
        """
        Args:
             width: bin width
             low: lower boundary
             up: upper boundary

        Returns:
            A histogram plot of dwell times
        """
        x = np.array(list(self.DwellTime.values()))
        x = x[x >= low]
        x = x[x <= up]
        bins = np.arange(min(x), max(x)+width, width)
        plt.figure(figsize=(16, 4))
        counts, bins, patch = plt.hist(self.DwellTime.values(), bins=bins, ec='k', linewidth=1.2, density=True,
                                       alpha=0.5)
        x = list(self.DwellTime.values())
        kde = stats.gaussian_kde(x)
        xx = np.linspace(0,max(self.DwellTime.values())+width,1000)
        plt.plot(xx, kde(xx))
        mids = (bins[1:]+bins[:-1])*0.5
        probs = counts/sum(counts)
        mean = sum(probs*mids)
        sd = np.sqrt(sum(probs*(mids - mean)**2))
        plt.xlabel('Dwell Time (ms)')
        plt.xlim(low,up)
        plt.ylabel('Probability Density')
        print('Number of events = ' + str(len(x)))
        print('Mean is ' + str(mean)+'ms' + u' \u00B1 ' + str(sd)+' ms')
        plt.show()

    def hist_curr_max(self, width, low, up):
        """
        Args:
            width: bin width
            low: lower boundary
            up: upper boundary

        Returns:
            A histogram plot of current values of the events using peak amplitude method
        """

        max_curr=[]
        for k,v in self.CountsExtract.items():
            max_curr.append(max(v))

        x=np.array(max_curr)
        x = x[x >= low]
        x = x[x <= up]
        bins = np.arange(min(x), max(x)+width, width)
        plt.figure(figsize=(16, 4))
        counts, bins, patch = plt.hist(x, bins=bins, ec='k', linewidth=1.2, density = True, alpha=0.5)
        kde = stats.gaussian_kde(x)
        xx=np.linspace(0, max(x)+width,1000)
        plt.plot(xx, kde(xx))
        mids = (bins[1:] + bins[:-1]) * 0.5 * 1e3
        probs = counts / sum(counts)
        mean = sum(probs * mids)
        sd = np.sqrt(sum(probs * (mids - mean) ** 2))
        plt.xlabel('Height (nA)')
        plt.xlim(low, up)
        plt.ylabel('Probability Density')
        print('Number of events = ' + str(len(x)))
        print('Mean is ' + str(mean) + 'pA' + u' \u00B1 ' + str(sd) + ' pA')
        plt.show()

    def hist_curr_cusum(self, width, low, up):
        """
        Args:
            width: bin width
            low: lower boundary
            up: upper boundary
        Returns:
            A histogram plot of current values of the events using the CUSUM method
        """
        max_curr_cusum = []
        for k,v in self.Fit.items():
            if len(v) >= 3:
                max_curr_cusum.append(max(v[1:-1])-np.mean([v[0], v[-1]]))

        x=np.array(max_curr_cusum)
        x = x[x >= low]
        x = x[x <= up]
        bins = np.arange(min(x), max(x) + width, width)
        plt.figure(figsize=(16, 4))
        counts, bins, patch = plt.hist(x, bins=bins, ec='k', linewidth=1.2, density = True, alpha=0.5)
        kde = stats.gaussian_kde(x)
        xx = np.linspace(0, max(x)+width, 1000)
        plt.plot(xx, kde(xx))
        mids = (bins[1:] + bins[:-1]) * 0.5 * 1e3
        probs = counts / sum(counts)
        mean = sum(probs * mids)
        sd = np.sqrt(sum(probs * (mids - mean) ** 2))
        plt.xlabel('Height (nA)')
        plt.xlim(low, up)
        plt.ylabel('Probability Density')
        print('Number of events = ' + str(len(x)))
        print('Mean is ' + str(mean) + 'pA' + u' \u00B1 ' + str(sd) + ' pA')
        plt.show()

    def hist_curr_adept(self, width, low, up):
        """
        Args:
             width: bin width
             low: lower boundary
             up: upper boundary
        Returns:
            A histogram plot of current values of the events using the ADEPT method
        """
        x = np.array(list(self.ADEPT_curr_max.values()))
        x = x[x >= low]
        x=x[x<=up]
        bins = np.arange(min(x), max(x) + width, width)
        plt.figure(figsize=(16, 4))
        counts, bins, patch = plt.hist(x, bins=bins, ec='k', linewidth=1.2, density=True, alpha=0.5)
        kde = stats.gaussian_kde(x)
        xx = np.linspace(0, max(x) + width, 1000)
        plt.plot(xx, kde(xx))
        mids = (bins[1:] + bins[:-1]) * 0.5 * 1e3
        probs = counts / sum(counts)
        mean = sum(probs * mids)
        sd = np.sqrt(sum(probs * (mids - mean) ** 2))
        plt.xlabel('Height (nA)')
        plt.xlim(low, up)
        plt.ylabel('Probability Density')
        print('Number of events = ' + str(len(x)))
        print('Mean is ' + str(mean) + 'pA' + u' \u00B1 ' + str(sd) + ' pA')
        plt.show()



def FitFuncTwo(t, a_j_r, a_j_d, i_o, u_j_r, u_j_d, t_j_r, t_j_d):
    Func = 0
    a_j = [a_j_r, a_j_d]
    u_j = [u_j_r, u_j_d]
    t_j = [t_j_r, t_j_d]

    for i in range(2):
        t1 = 1 - np.exp(-(t - u_j[i]) / t_j[i])
        Func += a_j[i] * t1 * np.heaviside((t - u_j[i]), 0.5)

    StepRes = i_o + Func

    return StepRes


def FitFuncThree(t, a_j_r, a_j_m, a_j_d, i_o, u_j_r, u_j_m, u_j_d, t_j_r, t_j_m, t_j_d):
    Func = np.zeros([len(t), ])

    a_j = np.array([a_j_r, a_j_m, a_j_d])
    t_j = np.array([t_j_r, t_j_m, t_j_d])
    u_j = np.array([u_j_r, u_j_m, u_j_d])

    for i in range(3):
        t1 = 1 - np.exp(u_j[i] - t / t_j[i])
        t1[np.isnan(t1)] = 0
        Func += a_j[i] * np.heaviside(t - u_j[i], 0.5) * t1

    StepRes = Func + i_o
    StepRes[np.isnan(StepRes)] = 0

    return StepRes

