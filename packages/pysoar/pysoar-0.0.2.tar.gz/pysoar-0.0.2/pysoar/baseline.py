import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt


def baseline(y,time, l, p):
    """
    Returns the smoothed signal as an array and the clean current

    Args:
        y: Raw signal
        time: time data points
        l: Poly-1 coefficient
        p: Poly-2 coefficient
    """

    m = len(y)
    mm = sparse.identity(m, dtype='int8', format='csr')

    for i in [0, 1]:
        mm = mm[1:] - mm[:-1]

    w = np.ones(m)
    for i in range(10):
        W = sparse.spdiags(w, 0, m, m)
        D = sparse.csr_matrix.transpose(mm)
        Z = W + l * D * mm
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)

    CountBase = y - z
    CountBase[CountBase < 0] = 0

    plt.figure(figsize=[12, 8])
    plt.plot(time, y)
    plt.plot(time, z, 'r')
    plt.ylabel('Current (nA)')
    plt.xlabel('Time (s)')
    plt.show()

    plt.figure(figsize=[12, 8])
    plt.plot(time, CountBase)
    plt.ylabel('Current (nA)')
    plt.xlabel('Time (s)')
    plt.show()

    return z, CountBase




