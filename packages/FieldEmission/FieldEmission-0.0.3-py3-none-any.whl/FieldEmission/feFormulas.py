from logging import exception
from dataManager import DataProvider as dPrvdr
import numpy as np
import math


def FowlerNordheim(DatMgr: dPrvdr, ColumnU, ColumnI, distance_m):
    # Create copys of U and I (also for predefining correct array-size)
    fnX = abs(DatMgr.GetColumn(ColumnU))  # Here still U!
    fnY = abs(DatMgr.GetColumn(ColumnI))  # Here still I!

    for iRow in range(len(fnX)):
        fnX[iRow] = distance_m / fnX[iRow]  # Convert d/U = 1/E
        fnY[iRow] = math.log(fnY[iRow] * math.pow(fnX[iRow], 2))  # Convert I -> fnY

    return np.transpose([fnX, fnY])
