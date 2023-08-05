import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date

def getChunk(data, chunk):
    chunks = [-1]+[x[0] for x in np.argwhere(np.isnan(data))]
    if chunk>=len(chunks):
        raise ValueError("The data does not contain enough chunk")
    else:
        chunks += [len(data)]
        return data[chunks[chunk]+1:chunks[chunk+1]]

def plotJV(res, hyst=False, ax=None):
    V = res['voltage'][0]
    I = res['current'][0]

    if ax is None:
        ax = plt.gca()
    numC = np.sum(np.isnan(V))
    if hyst and numC>1:
        for i in range(2):
            Vx = getChunk(V,i)
            UP = Vx[0]<Vx[-1]
            ax.plot(Vx, getChunk(I,i), label=["down","up"][UP])
    else:
        ax.plot(V, I)
    ax.set_xlabel("Voltage ["+res['voltage'][1]+"]")
    ax.set_ylabel("Current ["+res['current'][1]+"]")
    return ax
    
def flux2timestamp(ts):
    """
    convert a flux time stamp tuple to a python tuple.
    
    return (datetime object, fractional seconds)
    """
    return (datetime.fromtimestamp(ts[1]-2082844800), ts[0]/2**64)
    
def PT100res2temp(Rt, R0=100):
    """
    convert the resistivity measured of a PT100 to its equivalent temperature (in °C)
    """
    
    A = 0.003909
    B = -5.775e-7
    return (np.sqrt(A**2-4*B*(1-(Rt/R0)))-A)/(2*B)