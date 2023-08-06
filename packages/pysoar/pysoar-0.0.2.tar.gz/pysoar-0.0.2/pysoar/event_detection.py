import numpy as np
import ruptures as rpt
from pysoar.Translocations import Translocations

def event_detection(delta, sigma, BinDiff, BaselineLength, T_res, TiLow, TiHigh, Time_3, MaxLevel, CountBase):
    """
    Args:
         delta: Minimum rise/fall in current to be counted as a separate level
         sigma: Amount of standard deviation of the baseline current
         BinDiff: Minimum length for a level
         BaselineLength: Amount of baseline points taken into the consideration on each side of the event
         T_res: Time resolution
         TiLow: Array containing time at which the events start
         TiHigh: Array containing time at which the events ends
         Time_3: Time data points
         MaxLevel: Maximum number of change points
         CountBase: Current data points

    Returns:
        An object of Translocations class, containing the information about each event
    """

    dt=1e-9
    NumberOfEvents = len(TiLow)
    event = Translocations()
    Test_ti_Pad = {}
    CountBasePad = {}
    ti_event = {}
    icp2 = {}
    model = 'l2'
    std_bkg = {}

    for i in range(NumberOfEvents):
        CusumReferencedStartPoint = round(TiLow[i] / T_res + dt) - BaselineLength
        if CusumReferencedStartPoint < 0:
            CusumReferencedStartPoint = 0

        CusumReferencedEndPoint = round(TiHigh[i] / T_res + dt) + BaselineLength
        if CusumReferencedEndPoint > len(Time_3):
            CusumReferencedEndPoint = len(Time_3)

        StartPoint = round(TiLow[i] / T_res + dt) - 1
        EndPoint = round(TiHigh[i] / T_res + dt)

        Test_ti_Pad[i] = Time_3[CusumReferencedStartPoint:CusumReferencedEndPoint]
        CountBasePad[i] = CountBase[CusumReferencedStartPoint:CusumReferencedEndPoint]
        ti_event[i] = Time_3[StartPoint:EndPoint]

        t = Test_ti_Pad[i]
        x = CountBasePad[i]

        deltaT = np.diff(t)
        deltaT = deltaT[0]

        BinLow = round((TiLow[i] - min(t)) / deltaT + dt) - 8
        BinHigh = round((TiHigh[i] - min(t)) / deltaT + dt) + 8

        algo = rpt.Binseg(model=model).fit(x)
        my_bkps = algo.predict(n_bkps=MaxLevel)
        my_bkps = np.array(my_bkps) - 1
        icp2[i] = my_bkps

        icp2[i] = icp2[i][icp2[i] > BinLow]
        icp2[i] = icp2[i][icp2[i] < BinHigh]

        if len(icp2[i]) != 0:

            std_bkg[i] = np.std(x[:icp2[i][0] + 1])
            MEAN = Check(icp2[i], x, t)
            DIFFMean = np.diff(MEAN[:, 2])

            V1 = np.where(abs(DIFFMean) > std_bkg[i] * sigma)[0]
            icp2[i] = icp2[i][V1]
            MEAN = Check(icp2[i], x, t)

            DIFFBin = MEAN[:, 1] - MEAN[:, 0]
            DIFFBin = np.delete(DIFFBin, -1)
            icp2[i] = icp2[i][DIFFBin > BinDiff]
            MEAN = Check(icp2[i], x, t)

            while sum((abs(np.diff(MEAN[:, 2])) < delta) * 1) > 0:
                DIFFPk = abs(np.diff(MEAN[:, 2]))
                pol = DIFFPk > delta
                icp2[i] = icp2[i][pol]
                MEAN = Check(icp2[i], x, t)

            event.Fit[i] = (MEAN[:, 2])
            event.CountsExtract[i] = x
            event.TimeExtract[i] = t
            event.TimeEvent[i] = ti_event[i]
            event.MEAN[i] = MEAN
            event.icp[i] = icp2[i]
            event.NumberOfLevels[i] = len(icp2[i]) - 1
            event.DwellTime[i] = (TiHigh[i]-TiLow[i])*1000

            if len(event.Fit[i]) <= 3:
                event.NoSubPeaks[i] = 0
            else:
                event.NoSubPeaks[i] = len(event.Fit[i])-3

            event.EventBasefull[i] = CountBasePad[i]

            if event.NumberOfLevels[i] < 0:
                event.NumberOfLevels[i] = 0

            event.std[i] = std_bkg[i]
            event.PeakHeight[i] = max(event.CountsExtract[i]) - np.mean([np.mean(CountBase[np.arange(
                CusumReferencedStartPoint, StartPoint+1)]), np.mean(CountBase[np.arange(EndPoint,
                                                                                        CusumReferencedEndPoint+1)])])

        else:
            emp = np.empty((1, len(t)))
            emp[:] = np.nan
            event.Fit[i] = emp
            event.CountsExtract[i] = x
            event.TimeExtract[i] = t
            event.TimeEvent[i] = ti_event[i]
            event.EventBasefull[i] = CountBasePad[i]
            event.MEAN[i] = np.zeros((1, 13))
            event.icp[i] = []
            event.DwellTime[i] = (TiHigh[i] - TiLow[i]) * 1000
            event.PeakHeight[i] = max(event.CountsExtract[i]) - np.mean([
                np.mean(CountBase[np.arange(CusumReferencedStartPoint, StartPoint + 1)]),
                np.mean(CountBase[np.arange(EndPoint, CusumReferencedEndPoint + 1)])])

            event.NumberOfLevels[i] = 0
            event.Classification[i] = 0
            event.NoSubPeaks[i] = 0
            event.SubPeakLocation[i] = 0

    return event


def Check(icp3, x, t):
    K = len(icp3)
    nseg = K + 1
    istart = [0]
    istop = []

    MEAN = [[0 for i in range(13)] for j in range(nseg)]
    MEAN = np.array(MEAN, dtype=float)

    for i in icp3:
        istart.append(i)
        istop.append(i - 1)

    istop.append(len(x) - 1)

    for s in range(nseg):
        ix = np.arange(istart[s], istop[s] + 1)

        MEAN[s, 2] = np.mean(x[ix])
        MEAN[s, 3] = np.std(x[ix])
        MEAN[s, 0] = istart[s]
        MEAN[s, 1] = istop[s]
        MEAN[s, 4] = max(x[ix])
        MEAN[s, 5] = min(x[ix])

        MaxLoc = np.where(x[ix] == max(x[ix]))[0][0]
        MinLoc = np.where(x[ix] == min(x[ix]))[0][0]

        if s > 0:
            MEAN[s, 6] = MEAN[s, 2] - MEAN[s - 1, 2]
            MEAN[s, 10] = MEAN[s, 4] - MEAN[s - 1, 2]
        else:
            MEAN[s, 6] = 0
            MEAN[s, 11] = 0

        tt = t[ix]
        MEAN[s, 7] = tt[MaxLoc]
        MEAN[s, 8] = tt[MinLoc]

        deltaT = np.diff(t)
        deltaT = deltaT[0]

        MEAN[s, 9] = (MEAN[s, 1] - MEAN[s, 0]) * deltaT
        MEAN[s, 11] = tt[0]
        MEAN[s, 12] = tt[-1]

    return MEAN


def EventClassifier(MEAN):
    NoSubPeaks = 0
    SubPeakLocation = ''
    EventClass = 2.5

    BinaryClass = np.copy(MEAN[:, 6])
    BinaryClass[BinaryClass < 0] = 0
    BinaryClass[BinaryClass > 0] = 1
    BinaryClass = BinaryClass.astype(int)
    Classification = ''.join(str(i) for i in BinaryClass)

    if Classification == '010':
        NoSubPeaks = 0
        SubPeakLocation = ''

    elif Classification == '0100':
        if MEAN[2, 9] * EventClass < MEAN[1, 9]:
            NoSubPeaks = 0
            SubPeakLocation = ' '
        else:
            NoSubPeaks = 1
            SubPeakLocation = 'Start'

    elif Classification == '0110':
        if MEAN[2, 9] > MEAN[1, 9] * EventClass:
            NoSubPeaks = 0
            SubPeakLocation = ' '
        else:
            NoSubPeaks = 1
            SubPeakLocation = 'End'

    elif Classification == '01110':
        NoSubPeaks = 1
        SubPeakLocation = 'End'

    elif Classification == '01100':
        if MEAN[2, 9] > MEAN[1, 9] * EventClass and MEAN[3, 9] < MEAN[2, 9]:
            NoSubPeaks = 0
            SubPeakLocation = ' '
        else:
            NoSubPeaks = 1
            SubPeakLocation = 'Middle'

    elif Classification == '011100':
        NoSubPeaks = 1
        SubPeakLocation = 'Middle'

    elif Classification == '0111000':
        NoSubPeaks = 1
        SubPeakLocation = 'Middle'

    elif Classification == '011000':
        NoSubPeaks = 1
        SubPeakLocation = 'Middle'

    elif Classification == '01110000':
        NoSubPeaks = 1
        SubPeakLocation = 'Middle'

    elif Classification == '01010':
        NoSubPeaks = 2
        SubPeakLocation = 'Start End'

    elif Classification == '010100':
        NoSubPeaks = 2
        SubPeakLocation = 'Start Middle'

    elif Classification == '0101000':
        NoSubPeaks = 2
        SubPeakLocation = 'Start Middle'

    elif Classification == '011010':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle End'

    elif Classification == '0110100':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '01110100':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '011101000':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '011101100':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '011011000':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '011100100':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    elif Classification == '01101000':
        NoSubPeaks = 2
        SubPeakLocation = 'Middle Middle'

    else:
        NoPosSubPeaks = 25
        for j in range(3, NoPosSubPeaks + 1):

            P1 = np.tile('10', (1, j))[0]
            np.insert(P1, 0, '0')
            P1 = ''.join(str(i) for i in P1)

            P2 = np.tile('10', (1, j - 1))[0]
            np.insert(P2, 0, '0')
            np.insert(P2, -1, '100')
            P2 = ''.join(str(i) for i in P2)

            P3 = np.tile('10', (1, j - 1))[0]
            np.insert(P3, 0, '0')
            np.insert(P3, -1, '1000')
            P3 = ''.join(str(i) for i in P3)

            P4 = np.tile('10', (1, j))[0]
            np.insert(P4, 0, '01')
            P4 = ''.join(str(i) for i in P4)

            P5 = np.tile('10', (1, j - 1))[0]
            np.insert(P5, 0, '01')
            np.insert(P5, -1, '100')
            P5 = ''.join(str(i) for i in P5)

            A = []

            for i in [P1, P2, P3, P4, P5]:
                A.append((Classification == i) * 1)

            A = np.array(A)

            if sum(A) == 1:
                Loc = np.where(A == 1)[0][0]
                NoSubPeaks = j

                if Loc == 0:
                    SubPeakLocation = ['Start ' + ('Middle ') * j - 2 + 'End']

                elif Loc == 1:
                    SubPeakLocation = ['Start ' + ('Middle ') * j - 1]

                elif Loc == 2:
                    SubPeakLocation = ['Start ' + ('Middle ') * j - 1]

                elif Loc == 3:
                    SubPeakLocation = ['Start ' + ('Middle ') * j - 1 + 'End']

                elif Loc == 4:
                    SubPeakLocation = [('Middle ') * j]

                break

    return Classification, NoSubPeaks, SubPeakLocation



